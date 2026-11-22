#!/usr/bin/env python

import json
import os
import random
from pathlib import Path

import streamlit as st

from viper import urls
from viper.coders import Coder
from viper.dump import dump  # noqa: F401
from viper.io import InputOutput
from viper.main import main as cli_main
from viper.scrape import Scraper, has_playwright

I18N_DIR = Path(__file__).resolve().parent / "resources" / "i18n"
SUPPORTED_LANGUAGES = {"ko": "language_ko", "en": "language_en"}
DEFAULT_LANGUAGE = "ko"


def load_translations(lang):
    path = I18N_DIR / f"{lang}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


TRANSLATIONS = {lang: load_translations(lang) for lang in SUPPORTED_LANGUAGES}


class CaptureIO(InputOutput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lines = []

    def tool_output(self, *messages, log_only=False, bold=False):
        msg = " ".join(str(m) for m in messages) if messages else ""
        if not log_only:
            self.lines.append(msg)
        super().tool_output(*messages, log_only=log_only, bold=bold)

    def tool_error(self, msg="", strip=True):
        self.lines.append(str(msg))
        super().tool_error(msg, strip=strip)

    def tool_warning(self, msg=""):
        self.lines.append(str(msg))
        super().tool_warning(msg)

    def get_captured_lines(self):
        lines = self.lines
        self.lines = []
        return lines


def search(text=None):
    results = []
    for root, _, files in os.walk("viper"):
        for file in files:
            path = os.path.join(root, file)
            if not text or text in path:
                results.append(path)
    return results


# Keep state as a resource, which survives browser reloads (since Coder does too)
class State:
    def __init__(self):
        self.keys = set()

    def init(self, key, val=None):
        if key in self.keys:
            return False

        self.keys.add(key)
        setattr(self, key, val)
        return True


@st.cache_resource
def get_state():
    return State()


@st.cache_resource(show_spinner="Viper 초기화 중...")
def get_coder():
    coder = cli_main(return_coder=True)
    if not isinstance(coder, Coder):
        raise ValueError(coder)
    if not coder.repo:
        raise ValueError("GUI can currently only be used inside a git repo")

    io = CaptureIO(
        pretty=False,
        yes=True,
        dry_run=coder.io.dry_run,
        encoding=coder.io.encoding,
    )
    coder.io = io
    coder.commands.io = io
    coder.suggest_shell_commands = False

    for line in coder.get_announcements():
        coder.io.tool_output(line)

    return coder


class GUI:
    prompt = None
    prompt_as = "user"
    last_undo_empty = None
    recent_msgs_empty = None
    web_content_empty = None

    @property
    def lang(self):
        lang = st.session_state.get("language", DEFAULT_LANGUAGE)
        return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE

    def t(self, key, **kwargs):
        lang = self.lang
        text = TRANSLATIONS.get(lang, {}).get(key)
        if text is None:
            text = TRANSLATIONS.get("en", {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def announce(self):
        lines = self.coder.get_announcements()
        lines = "  \n".join(lines)
        return lines

    def show_edit_info(self, edit):
        commit_hash = edit.get("commit_hash")
        commit_message = edit.get("commit_message")
        diff = edit.get("diff")
        fnames = edit.get("fnames")
        if fnames:
            fnames = sorted(fnames)

        if not commit_hash and not fnames:
            return

        show_undo = False
        res = ""
        if commit_hash:
            res += self.t("commit_info", commit_hash=commit_hash, commit_message=commit_message)
            if commit_hash == self.coder.last_aider_commit_hash:
                show_undo = True

        if fnames:
            fnames = [f"`{fname}`" for fname in fnames]
            fnames = ", ".join(fnames)
            res += self.t("applied_edits_to", fnames=fnames)

        if diff:
            with st.expander(res):
                st.code(diff, language="diff")
                if show_undo:
                    self.add_undo(commit_hash)
        else:
            with st.container(border=True):
                st.write(res)
                if show_undo:
                    self.add_undo(commit_hash)

    def add_undo(self, commit_hash):
        if self.last_undo_empty:
            self.last_undo_empty.empty()

        self.last_undo_empty = st.empty()
        undone = self.state.last_undone_commit_hash == commit_hash
        if not undone:
            with self.last_undo_empty:
                if self.button(
                    self.t("undo_commit", commit_hash=commit_hash), key=f"undo_{commit_hash}"
                ):
                    self.do_undo(commit_hash)

    def do_language_menu(self):
        lang_codes = list(SUPPORTED_LANGUAGES.keys())
        current_lang = self.lang
        current_index = lang_codes.index(current_lang) if current_lang in lang_codes else 0
        st.selectbox(
            self.t("language_label"),
            options=lang_codes,
            index=current_index,
            format_func=lambda code: self.t(f"language_{code}"),
            key="language",
        )

    def do_sidebar(self):
        with st.sidebar:
            st.title(self.t("app_title"))
            self.do_add_to_chat()
            self.do_recent_msgs()
            self.do_clear_chat_history()

            st.warning(self.t("experimental_warning"))
            self.do_language_menu()

    def do_settings_tab(self):
        pass

    def do_recommended_actions(self):
        text = "Viper works best when your code is stored in a git repo.  \n"
        text += f"[See the FAQ for more info]({urls.git})"

        with st.expander("Recommended actions", expanded=True):
            with st.popover("Create a git repo to track changes"):
                st.write(text)
                self.button("Create git repo", key=random.random(), help="?")

            with st.popover("Update your `.gitignore` file"):
                st.write("It's best to keep aider's internal files out of your git repo.")
                self.button("Add `.aider*` to `.gitignore`", key=random.random(), help="?")

    def do_add_to_chat(self):
        self.do_add_files()
        self.do_add_web_page()

    def do_add_files(self):
        fnames = st.multiselect(
            self.t("add_files_to_chat"),
            self.coder.get_all_relative_files(),
            default=self.state.initial_inchat_files,
            placeholder=self.t("files_to_edit_placeholder"),
            disabled=self.prompt_pending(),
            help=self.t("files_to_edit_help"),
        )

        for fname in fnames:
            if fname not in self.coder.get_inchat_relative_files():
                self.coder.add_rel_fname(fname)
                self.info(self.t("added_file_to_chat", fname=fname))

        for fname in self.coder.get_inchat_relative_files():
            if fname not in fnames:
                self.coder.drop_rel_fname(fname)
                self.info(self.t("removed_file_from_chat", fname=fname))

    def do_add_web_page(self):
        with st.popover(self.t("add_web_page_to_chat")):
            self.do_web()

    def do_add_image(self):
        with st.popover(self.t("add_image")):
            st.file_uploader(self.t("image_file"), disabled=self.prompt_pending())

    def do_run_shell(self):
        with st.popover(self.t("run_shell_commands")):
            st.markdown(self.t("run_shell_commands_desc"))
            st.text_input(self.t("command_label"))
            st.radio(
                self.t("share_command_output"),
                [
                    self.t("share_output_review"),
                    self.t("share_output_auto_fail"),
                ],
            )
            st.selectbox(
                self.t("recent_commands"),
                [
                    "my_app.py --doit",
                    "my_app.py --cleanup",
                ],
                disabled=self.prompt_pending(),
            )

    def do_tokens_and_cost(self):
        with st.expander(self.t("tokens_and_costs"), expanded=True):
            pass

    def do_show_token_usage(self):
        with st.popover(self.t("show_token_usage")):
            st.write("hi")

    def do_clear_chat_history(self):
        text = self.t("clear_chat_history_help")
        if self.button(self.t("clear_chat_history"), help=text):
            self.coder.done_messages = []
            self.coder.cur_messages = []
            self.info(self.t("cleared_chat_history"))

    def do_show_metrics(self):
        st.metric("Cost of last message send & reply", "$0.0019", help="foo")
        st.metric("Cost to send next message", "$0.0013", help="foo")
        st.metric("Total cost this session", "$0.22")

    def do_git(self):
        with st.expander(self.t("git"), expanded=False):
            self.button(self.t("commit_pending_changes"))
            with st.popover(self.t("run_git_command")):
                st.markdown(f"## {self.t('run_git_command')}")
                st.text_input("git", value="git ")
                self.button(self.t("run"))
                st.selectbox(
                    self.t("recent_git_commands"),
                    [
                        "git checkout -b experiment",
                        "git stash",
                    ],
                    disabled=self.prompt_pending(),
                )

    def do_recent_msgs(self):
        if not self.recent_msgs_empty:
            self.recent_msgs_empty = st.empty()

        if self.prompt_pending():
            self.recent_msgs_empty.empty()
            self.state.recent_msgs_num += 1

        with self.recent_msgs_empty:
            self.old_prompt = st.selectbox(
                self.t("recent_chat_message"),
                self.state.input_history,
                placeholder=self.t("recent_chat_message_placeholder"),
                index=None,
                key=f"recent_msgs_{self.state.recent_msgs_num}",
                disabled=self.prompt_pending(),
            )
            if self.old_prompt:
                self.prompt = self.old_prompt

    def do_messages_container(self):
        self.messages = st.container()

        with self.messages:
            for msg in self.state.messages:
                role = msg["role"]

                if role == "edit":
                    self.show_edit_info(msg)
                elif role == "info":
                    st.info(msg["content"])
                elif role == "text":
                    text = msg["content"]
                    line = text.splitlines()[0]
                    with self.messages.expander(line):
                        st.text(text)
                elif role in ("user", "assistant"):
                    with st.chat_message(role):
                        st.write(msg["content"])
                else:
                    st.dict(msg)

    def initialize_state(self):
        messages = [
            dict(role="info", content=self.announce()),
            dict(role="assistant", content=self.t("assistant_greeting")),
        ]

        self.state.init("messages", messages)
        self.state.init("last_aider_commit_hash", self.coder.last_aider_commit_hash)
        self.state.init("last_undone_commit_hash")
        self.state.init("recent_msgs_num", 0)
        self.state.init("web_content_num", 0)
        self.state.init("prompt")
        self.state.init("scraper")

        self.state.init("initial_inchat_files", self.coder.get_inchat_relative_files())

        if "input_history" not in self.state.keys:
            input_history = list(self.coder.io.get_input_history())
            seen = set()
            input_history = [x for x in input_history if not (x in seen or seen.add(x))]
            self.state.input_history = input_history
            self.state.keys.add("input_history")

    def button(self, args, **kwargs):
        "Create a button, disabled if prompt pending"
        if self.prompt_pending():
            kwargs["disabled"] = True

        return st.button(args, **kwargs)

    def __init__(self):
        self.coder = get_coder()
        self.state = get_state()

        self.coder.yield_stream = True
        self.coder.stream = True
        self.coder.pretty = False

        self.initialize_state()

        self.do_messages_container()
        self.do_sidebar()

        user_inp = st.chat_input(self.t("chat_placeholder"))
        if user_inp:
            self.prompt = user_inp

        if self.prompt_pending():
            if st.session_state.get("_viper_processing_prompt"):
                self.process_chat()
            else:
                self.state.prompt = None
                st.session_state.pop("_viper_processing_prompt", None)

        if not self.prompt:
            st.session_state.pop("_viper_processing_prompt", None)
            return

        self.state.prompt = self.prompt
        st.session_state["_viper_processing_prompt"] = True

        if self.prompt_as == "user":
            self.coder.io.add_to_input_history(self.prompt)

        self.state.input_history.append(self.prompt)

        if self.prompt_as:
            self.state.messages.append({"role": self.prompt_as, "content": self.prompt})
        if self.prompt_as == "user":
            with self.messages.chat_message("user"):
                st.write(self.prompt)
        elif self.prompt_as == "text":
            line = self.prompt.splitlines()[0]
            line += "..."
            with self.messages.expander(line):
                st.text(self.prompt)

        st.rerun()

    def prompt_pending(self):
        return self.state.prompt is not None

    def cost(self):
        cost = random.random() * 0.003 + 0.001
        st.caption(f"${cost:0.4f}")

    def process_chat(self):
        prompt = self.state.prompt
        self.state.prompt = None

        self.num_reflections = 0
        self.max_reflections = 3

        while prompt:
            with self.messages.chat_message("assistant"):
                try:
                    st.caption(
                        self.t(
                            "debug_model_info",
                            model=getattr(self.coder.main_model, "name", "?"),
                            stream=self.coder.stream,
                            pretty=self.coder.pretty,
                            yield_stream=getattr(self.coder, "yield_stream", "?"),
                            edit_format=getattr(self.coder, "edit_format", "?"),
                        )
                    )

                    stream_stats = {"chunks": 0, "chars": 0}

                    def debug_stream():
                        try:
                            for chunk in self.coder.run_stream(prompt):
                                if chunk is None:
                                    continue
                                text_chunk = chunk if isinstance(chunk, str) else str(chunk)
                                stream_stats["chunks"] += 1
                                stream_stats["chars"] += len(text_chunk)
                                yield text_chunk
                        except Exception as stream_err:
                            st.exception(stream_err)
                            raise

                    res = st.write_stream(debug_stream())

                    st.caption(
                        self.t(
                            "debug_stream_finished",
                            chunks=stream_stats["chunks"],
                            chars=stream_stats["chars"],
                        )
                    )
                    if stream_stats["chunks"] == 0:
                        st.warning(self.t("debug_no_chunks"))

                    if not res:
                        partial = getattr(self.coder, "partial_response_content", "") or ""
                        if partial:
                            st.info(self.t("debug_partial_response"))
                            st.write(partial)
                            res = partial
                        else:
                            st.error(self.t("debug_empty_response"))

                        try:
                            captured = self.coder.commands.io.get_captured_lines()
                            if captured:
                                with st.expander(self.t("debug_captured_log"), expanded=True):
                                    st.code("\n".join(captured))
                        except Exception as log_err:
                            st.caption(self.t("debug_captured_log_read_failed", error=log_err))

                    self.state.messages.append({"role": "assistant", "content": res or ""})
                except Exception as e:
                    st.exception(e)
                    self.info(self.t("debug_error", error=f"{type(e).__name__}: {e}"))
                    try:
                        captured = self.coder.commands.io.get_captured_lines()
                        if captured:
                            self.info(self.t("debug_captured_log_label", log="\n".join(captured)), echo=True)
                    except Exception:
                        pass
                    break

            prompt = None

    def info(self, message, echo=True):
        info = dict(role="info", content=message)
        self.state.messages.append(info)

        if echo:
            self.messages.info(message)

    def do_web(self):
        st.markdown(self.t("add_web_page_desc"))

        if not self.web_content_empty:
            self.web_content_empty = st.empty()

        if self.prompt_pending():
            self.web_content_empty.empty()
            self.state.web_content_num += 1

        with self.web_content_empty:
            self.web_content = st.text_input(
                "URL",
                placeholder=self.t("url_placeholder"),
                key=f"web_content_{self.state.web_content_num}",
            )

        if not self.web_content:
            return

        url = self.web_content

        if not self.state.scraper:
            self.state.scraper = Scraper(print_error=self.info, playwright_available=has_playwright())

        content = self.state.scraper.scrape(url) or ""
        if content.strip():
            content = f"{url}\n\n" + content
            self.prompt = content
            self.prompt_as = "text"
        else:
            self.info(self.t("no_web_content", url=url))
            self.web_content = None

    def do_undo(self, commit_hash):
        self.last_undo_empty.empty()

        if (
            self.state.last_aider_commit_hash != commit_hash
            or self.coder.last_aider_commit_hash != commit_hash
        ):
            self.info(f"Commit `{commit_hash}` is not the latest commit.")
            return

        self.coder.commands.io.get_captured_lines()
        reply = self.coder.commands.cmd_undo(None)
        lines = self.coder.commands.io.get_captured_lines()

        lines = "\n".join(lines)
        lines = lines.splitlines()
        lines = "  \n".join(lines)
        self.info(lines, echo=False)

        self.state.last_undone_commit_hash = commit_hash

        if reply:
            self.prompt_as = None
            self.prompt = reply


def gui_main():
    st.set_page_config(
        layout="wide",
        page_title="Viper",
        page_icon=urls.favicon,
        menu_items={
            "Get Help": urls.website,
            "Report a bug": "https://github.com/matthewb2/viper/issues",
            "About": "# Viper\n브라우저에서 AI 페어 프로그래밍.",
        },
    )

    st.markdown(
        """
        <style>
        header [data-testid="stHeaderActionElements"] { display: none !important; }
        [data-testid="stMainBlockContainer"] {
            margin-top: -50px !important;
        }
        
        [data-testid="stSidebarUserContent"] {
            margin-top: -50px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    GUI()


if __name__ == "__main__":
    gui_main()