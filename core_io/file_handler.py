import os

class FileHandler:
    def __init__(self):
        self.working_files = set()

    def add_file(self, file_path):
        normalized_path = os.path.normpath(file_path)
        self.working_files.add(normalized_path)
        return True

    def get_all_contexts(self):
        contexts = {}
        for path in self.working_files:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    contexts[path] = f.read()
        return contexts

    def apply_edits(self, ai_text):
        results = []
        lines = ai_text.split('\n')
        
        current_file = None
        mode = None
        search_block = []
        replace_block = []

        for line in lines:
            line_content = line.strip()
            
            # 1. 파일 경로 찾기 (공백/특수문자 제거 후 FILE: 확인)
            if "FILE:" in line_content:
                current_file = line_content.split("FILE:")[1].split("<<<<")[0].strip()
                # 만약 같은 줄에 <<<< SEARCH가 있다면 모드 전환
                if "<<<< SEARCH" in line_content:
                    mode = "SEARCH"
                    search_block = []
                continue

            # 2. 모드 전환 확인
            if "<<<< SEARCH" in line_content and mode is None:
                mode = "SEARCH"
                search_block = []
                continue
            elif "====" in line_content and mode == "SEARCH":
                mode = "REPLACE"
                replace_block = []
                continue
            elif ">>>> REPLACE" in line_content and mode == "REPLACE":
                # 블록 완성 -> 파일 수정 실행
                if current_file:
                    res = self._execute_edit(current_file, "\n".join(search_block), "\n".join(replace_block))
                    results.append(res)
                # 초기화
                current_file = None
                mode = None
                continue

            # 3. 내용 수집
            if mode == "SEARCH":
                search_block.append(line)
            elif mode == "REPLACE":
                replace_block.append(line)

        if not results:
            return ["[yellow]시스템: 수정 형식을 찾지 못했습니다. (파싱 실패)[/yellow]"]
        return results

    def _execute_edit(self, file_path, search, replace):
        file_path = os.path.normpath(file_path.strip())
        search = search.strip()
        replace = replace.strip()

        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f: f.write("")

        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # 수정 로직: SEARCH가 비어있으면 전체 교체, 있으면 해당 부분 교체
        if not search:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(replace)
            return f"[green]✔ {file_path} 전체 수정 완료[/green]"
        elif search in content:
            new_content = content.replace(search, replace)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return f"[green]✔ {file_path} 부분 수정 완료[/green]"
        else:
            return f"[red]✘ {file_path} 수정 실패 (SEARCH 문구 불일치)[/red]"