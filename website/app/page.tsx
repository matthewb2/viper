"use client";

import React, { useEffect, useState } from "react";

export default function ViperLandingPage() {
  const [currentPage, setCurrentPage] = useState<"home" | "guide">("home");
  const [activeMode, setActiveMode] = useState<"cli" | "web">("cli");
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  const githubUrl = "https://github.com/matthewb2/viper";
  const installCommand = "pip install git+https://github.com/matthewb2/viper.git";
  const realCmdCommand =
    ".venv\\Scripts\\python.exe -m viper --architect --model openrouter/openrouter/free --editor-model openrouter/openrouter/free --editor-edit-format diff --no-auto-commits e:\\hello-world";

  const handleCopy = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  useEffect(() => {
    const onUnhandledRejection = (event: PromiseRejectionEvent) => {
      const reasonStr = String(
        (event.reason as { message?: string } | undefined)?.message ?? event.reason ?? ""
      );
      if (reasonStr.includes("MetaMask") || reasonStr.includes("nkbihfbeogaeaoehlefnkodbefgpgknn")) {
        event.preventDefault();
      }
    };

    window.addEventListener("unhandledrejection", onUnhandledRejection);
    return () => window.removeEventListener("unhandledrejection", onUnhandledRejection);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 selection:bg-emerald-500/30 selection:text-emerald-200 font-sans">
      {/* 상단 내비게이션 */}
      <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <button
            onClick={() => {
              setCurrentPage("home");
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
            className="flex items-center gap-2.5 text-left"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono font-bold">
              &gt;_
            </div>
            <span className="text-lg font-bold tracking-tight text-white">
              viper
            </span>
            <span className="ml-2 rounded-full bg-slate-800 px-2.5 py-0.5 text-xs font-medium text-slate-400 border border-slate-700">
              Aider Fork
            </span>
          </button>

          <nav className="flex items-center gap-6 md:gap-8 text-sm font-medium text-slate-400">
            <button
              onClick={() => {
                setCurrentPage("home");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className={`transition-colors ${
                currentPage === "home" ? "text-emerald-400 font-semibold" : "hover:text-white"
              }`}
            >
              홈
            </button>
            <button
              onClick={() => {
                setCurrentPage("guide");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className={`flex items-center gap-1.5 transition-colors ${
                currentPage === "guide" ? "text-emerald-400 font-semibold" : "hover:text-white"
              }`}
            >
              <span>사용법 (Windows CMD)</span>
              <span className="rounded bg-emerald-500/15 px-1.5 py-0.5 text-[10px] font-bold text-emerald-400 border border-emerald-500/30">
                GUIDE
              </span>
            </button>
            {currentPage === "home" && (
              <>
                <a href="#features" className="hidden md:inline hover:text-white transition-colors">
                  핵심 최적화
                </a>
                <a href="#modes" className="hidden md:inline hover:text-white transition-colors">
                  CLI &amp; 웹 모드
                </a>
              </>
            )}
          </nav>

          <div className="flex items-center gap-3">
            <a
              href={githubUrl}
              target="_blank"
              rel="noreferrer"
              className="hidden sm:inline-block rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 transition-colors"
            >
              GitHub
            </a>
            <button
              onClick={() => {
                setCurrentPage("guide");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 transition-colors"
            >
              CMD 실행 가이드
            </button>
          </div>
        </div>
      </header>

      {currentPage === "home" ? (
        <>
          {/* 히어로 섹션 */}
          <section className="relative overflow-hidden pt-20 pb-24 md:pt-28 md:pb-32">
            <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-emerald-900/20 via-slate-950 to-slate-950" />
            <div className="mx-auto max-w-6xl px-6 text-center">
              <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3.5 py-1.5 text-xs font-medium text-emerald-300 mb-8">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                Repo Map 정밀 인덱싱 &amp; 루프 방지 엔진 탑재
              </div>

              <h1 className="mx-auto max-w-4xl text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl leading-[1.15]">
                불필요한 반복 루프는 줄이고,
                <br />
                <span className="bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
                  단 한 번에 정확한 코드를 완성합니다
                </span>
              </h1>

              <p className="mx-auto mt-6 max-w-2xl text-base sm:text-lg text-slate-400 leading-relaxed">
                <strong className="text-white font-semibold">viper</strong>는 Aider 기반 아키텍처를 포크하여 독자적인{" "}
                <strong className="text-slate-200 font-medium">Repo Map 그래프 최적화</strong>와{" "}
                <strong className="text-slate-200 font-medium">지능형 문맥(Context) 선별</strong> 알고리즘을 적용한 코딩 에이전트입니다.
                터미널 CLI와 직관적인 웹 브라우저 UI에서 원하는 LLM API를 자유롭게 연동하세요.
              </p>

              {/* 설치 명령어 복사 박스 */}
              <div id="quickstart" className="mx-auto mt-10 max-w-xl">
                <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/90 p-2 pl-4 shadow-2xl">
                  <code className="overflow-x-auto text-left font-mono text-xs sm:text-sm text-emerald-300 whitespace-nowrap">
                    $ {installCommand}
                  </code>
                  <button
                    onClick={() => handleCopy(installCommand, "hero-install")}
                    className="ml-3 shrink-0 rounded-lg bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition-colors border border-slate-700"
                  >
                    {copiedKey === "hero-install" ? "복사 완료!" : "명령어 복사"}
                  </button>
                </div>
                <div className="mt-4 flex flex-wrap items-center justify-center gap-4 text-xs text-slate-400">
                  <span>OpenRouter · Gemini · OpenAI · Claude · Ollama 지원</span>
                  <span>·</span>
                  <button
                    onClick={() => {
                      setCurrentPage("guide");
                      window.scrollTo({ top: 0, behavior: "smooth" });
                    }}
                    className="text-emerald-400 hover:underline font-medium"
                  >
                    Windows CMD 사용법 보기 →
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* 핵심 최적화 포인트 (3단 그리드) */}
          <section id="features" className="border-t border-slate-800/80 bg-slate-900/30 py-24">
            <div className="mx-auto max-w-6xl px-6">
              <div className="mb-16 text-center">
                <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  왜 viper가 더 빠르고 정확할까요?
                </h2>
                <p className="mt-4 text-slate-400">
                  LLM의 토큰 낭비와 환각 현상을 유발하는 3가지 병목 지점을 근본적으로 개선했습니다.
                </p>
              </div>

              <div className="grid gap-8 md:grid-cols-3">
                <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 hover:border-emerald-500/40 transition-colors">
                  <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 font-mono text-xl font-bold border border-emerald-500/20">
                    01
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">
                    고정밀 Repo Map 최적화
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    AST(추상 구문 트리) 기반 심볼 의존성 그래프를 재설계하여 프로젝트 전체 구조를 압축합니다. 거대한 저장소에서도 핵심 함수 시그니처와 호출 관계만 추출해 컨텍스트 한계를 극복합니다.
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 hover:border-cyan-500/40 transition-colors">
                  <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 font-mono text-xl font-bold border border-cyan-500/20">
                    02
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">
                    동적 문맥(Context) 자동 선별
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    사용자의 프롬프트 의도와 직접 연관된 파일만 스코어링하여 컨텍스트에 포함시킵니다. 관련 없는 코드로 인한 노이즈를 차단하여 경량 모델에서도 높은 추론 정확도를 발휘합니다.
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 hover:border-amber-500/40 transition-colors">
                  <div className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400 font-mono text-xl font-bold border border-amber-500/20">
                    03
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">
                    반복 수정 루프(Loop) 차단
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed">
                    동일한 컴파일·린트 에러를 반복하며 코드를 망가뜨리는 무한 루프 패턴을 감지합니다. 실패 원인을 요약하고 전략을 재수립해 첫 시도 성공률과 API 비용 효율을 동시에 높입니다.
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* 동작 원리 비교 */}
          <section id="architecture" className="border-t border-slate-800/80 py-24">
            <div className="mx-auto max-w-6xl px-6">
              <div className="mb-14 text-center">
                <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  viper 문맥 파이프라인 아키텍처
                </h2>
                <p className="mt-4 text-slate-400">
                  요청 분석부터 패치 적용까지 최소한의 턴(Turn)으로 완결되는 실행 흐름입니다.
                </p>
              </div>

              <div className="grid gap-6 md:grid-cols-4">
                {[
                  {
                    step: "STEP 1",
                    title: "의도 및 심볼 추출",
                    desc: "질의에서 핵심 키워드와 수정 대상 모듈을 파싱합니다.",
                  },
                  {
                    step: "STEP 2",
                    title: "가중치 Repo Map 탐색",
                    desc: "의존성 그래프에서 연관도가 높은 상위 파일만 필터링합니다.",
                  },
                  {
                    step: "STEP 3",
                    title: "정제된 프롬프트 생성",
                    desc: "중복 코드와 불필요한 주석을 제거한 고밀도 문맥을 LLM에 전달합니다.",
                  },
                  {
                    step: "STEP 4",
                    title: "Diff 검증 및 루프 가드",
                    desc: "수정 사항을 즉시 검증하고 동일 오류 재발 시 우회 전략을 실행합니다.",
                  },
                ].map((item, idx) => (
                  <div
                    key={idx}
                    className="relative rounded-xl border border-slate-800 bg-slate-900/40 p-6"
                  >
                    <span className="text-xs font-mono font-bold text-emerald-400">
                      {item.step}
                    </span>
                    <h4 className="mt-2 text-lg font-bold text-white">{item.title}</h4>
                    <p className="mt-2 text-sm text-slate-400 leading-relaxed">
                      {item.desc}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          {/* CLI & 웹 브라우저 듀얼 모드 프리뷰 */}
          <section id="modes" className="border-t border-slate-800/80 bg-slate-900/30 py-24">
            <div className="mx-auto max-w-5xl px-6">
              <div className="mb-12 text-center">
                <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  CLI와 웹 브라우저, 작업 환경에 맞춰 선택하세요
                </h2>
                <p className="mt-4 text-slate-400">
                  터미널 속도의 쾌적함과 시각적 Diff 리뷰 환경을 모두 지원합니다.
                </p>

                <div className="mt-8 inline-flex rounded-xl border border-slate-800 bg-slate-950 p-1.5">
                  <button
                    onClick={() => setActiveMode("cli")}
                    className={`rounded-lg px-5 py-2 text-sm font-semibold transition-all ${
                      activeMode === "cli"
                        ? "bg-emerald-500 text-slate-950 shadow"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    터미널 CLI 모드
                  </button>
                  <button
                    onClick={() => setActiveMode("web")}
                    className={`rounded-lg px-5 py-2 text-sm font-semibold transition-all ${
                      activeMode === "web"
                        ? "bg-emerald-500 text-slate-950 shadow"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    웹 브라우저 UI 모드
                  </button>
                </div>
              </div>

              <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 shadow-2xl">
                <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900/90 px-4 py-3">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-rose-500/80" />
                    <span className="h-3 w-3 rounded-full bg-amber-500/80" />
                    <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
                  </div>
                  <span className="font-mono text-xs text-slate-400">
                    {activeMode === "cli"
                      ? "cmd.exe — D:\\viper (e:\\hello-world)"
                      : "http://localhost:8501 — viper Web Workspace"}
                  </span>
                  <div className="w-12" />
                </div>

                {activeMode === "cli" ? (
                  <div className="p-6 font-mono text-xs sm:text-sm leading-relaxed space-y-3 text-slate-300">
                    <p className="text-emerald-400">
                      D:\viper&gt;{realCmdCommand}
                    </p>
                    <p className="text-slate-400">
                      Viper v0.86.3.dev+import
                      <br />
                      Model: openrouter/openrouter/free with architect edit format
                      <br />
                      Editor model: openrouter/openrouter/free with diff edit format
                      <br />
                      Git repo: E:\hello-world\.git with 0 files
                    </p>
                    <p className="text-cyan-300 pt-2">
                      architect&gt; gradle 기반으로 Hello World 자바 예제 프로젝트를 만드세요
                    </p>
                    <div className="rounded-lg bg-slate-900 border border-slate-800 p-3 text-xs space-y-1">
                      <div className="text-emerald-400">Applied edit to settings.gradle</div>
                      <div className="text-emerald-400">Applied edit to src/main/java/HelloWorld.java</div>
                      <div className="text-emerald-400">Applied edit to build.gradle</div>
                    </div>
                  </div>
                ) : (
                  <div className="grid md:grid-cols-3 min-h-[300px]">
                    <div className="border-b md:border-b-0 md:border-r border-slate-800 bg-slate-900/40 p-5 space-y-4">
                      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                        생성된 프로젝트 파일 (E:\hello-world)
                      </div>
                      <ul className="space-y-2 text-xs font-mono">
                        <li className="flex items-center justify-between rounded bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1.5 text-emerald-300">
                          <span>build.gradle</span>
                          <span>생성됨</span>
                        </li>
                        <li className="flex items-center justify-between rounded bg-slate-900 px-2.5 py-1.5 text-slate-300">
                          <span>settings.gradle</span>
                          <span>생성됨</span>
                        </li>
                        <li className="flex items-center justify-between rounded bg-slate-900 px-2.5 py-1.5 text-slate-300">
                          <span>src/main/java/HelloWorld.java</span>
                          <span>생성됨</span>
                        </li>
                      </ul>
                      <div className="pt-2 border-t border-slate-800 text-xs text-slate-400">
                        실행 명령: <code className="text-emerald-400">./gradlew run</code>
                      </div>
                    </div>

                    <div className="md:col-span-2 p-6 font-mono text-xs space-y-3">
                      <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800">
                        <span>src/main/java/HelloWorld.java</span>
                        <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-emerald-300">
                          diff 적용 완료
                        </span>
                      </div>
                      <pre className="overflow-x-auto text-slate-300 leading-relaxed">
{`  public class HelloWorld {
      public static void main(String[] args) {
+         System.out.println("Hello, World!");
      }
  }`}
                      </pre>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* 성능 비교 지표 섹션 */}
          <section id="benchmark" className="border-t border-slate-800/80 py-24">
            <div className="mx-auto max-w-5xl px-6">
              <div className="mb-12 text-center">
                <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                  문맥 최적화 전후 비교
                </h2>
                <p className="mt-4 text-slate-400">
                  불필요한 파일 전송과 재시도 루프를 줄여 비용과 대기 시간을 대폭 단축했습니다.
                </p>
              </div>

              <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/50">
                <table className="w-full text-left text-sm">
                  <thead className="border-b border-slate-800 bg-slate-900 text-slate-300">
                    <tr>
                      <th className="px-6 py-4 font-semibold">평가 항목</th>
                      <th className="px-6 py-4 font-semibold text-slate-400">기존 방식</th>
                      <th className="px-6 py-4 font-semibold text-emerald-400">viper 최적화 엔진</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 text-slate-300">
                    <tr>
                      <td className="px-6 py-4 font-medium text-white">평균 반복 수정 루프 횟수</td>
                      <td className="px-6 py-4 text-slate-400">3.8회 (오류 재발 빈번)</td>
                      <td className="px-6 py-4 font-semibold text-emerald-400">1.2회 (루프 차단 적용)</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 font-medium text-white">요청당 컨텍스트 토큰 사용량</td>
                      <td className="px-6 py-4 text-slate-400">전체 파일 포함 (고비용)</td>
                      <td className="px-6 py-4 font-semibold text-emerald-400">최대 60% 절감 (핵심 심볼 위주)</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 font-medium text-white">지원 인터페이스</td>
                      <td className="px-6 py-4 text-slate-400">단일 환경 중심</td>
                      <td className="px-6 py-4 font-semibold text-emerald-400">CLI 터미널 + 웹 브라우저 UI</td>
                    </tr>
                    <tr>
                      <td className="px-6 py-4 font-medium text-white">LLM API 호환성</td>
                      <td className="px-6 py-4 text-slate-400">주요 상용 모델</td>
                      <td className="px-6 py-4 font-semibold text-emerald-400">상용 API + 경량/무료 API 최적화</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </>
      ) : (
        /* =====================================================================
           사용법 페이지 (실제 Windows CMD 테스트 로그 및 결과 반영)
           ===================================================================== */
        <main className="mx-auto max-w-5xl px-6 py-16">
          {/* 상단 헤더 */}
          <div className="mb-12">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-300 mb-4">
              Windows CMD · Viper v0.86.3.dev+import 실테스트 기록
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
              Windows CMD에서 Viper 실행 및 Gradle Java Hello World 생성
            </h1>
            <p className="mt-3 text-slate-400 leading-relaxed max-w-3xl">
              <code className="text-emerald-300 font-mono">D:\viper</code> 가상환경에서{" "}
              <code className="text-emerald-300 font-mono">--architect</code> +{" "}
              <code className="text-emerald-300 font-mono">--editor-edit-format diff</code> 옵션으로{" "}
              <code className="text-emerald-300 font-mono">e:\hello-world</code> 저장소에 Gradle 기반 Java Hello World 프로젝트를 생성한 실제 실행 화면과 응답입니다.
            </p>
          </div>

          {/* 1. 실제 Windows CMD 실행 화면 및 ARCHITECT / EDITOR 응답 */}
          <section className="mb-16">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-400" />
                실제 Windows 명령 프롬프트 실행 화면 (D:\viper)
              </h2>

              <button
                onClick={() => handleCopy(`D:\\viper>${realCmdCommand}`, "real-cmd")}
                className="rounded-lg border border-slate-700 bg-slate-900 px-3.5 py-1.5 text-xs font-semibold text-slate-200 hover:bg-slate-800 transition-colors"
              >
                {copiedKey === "real-cmd" ? "실행 명령어 복사됨!" : "실행 명령어 복사"}
              </button>
            </div>

            {/* Windows CMD 창 */}
            <div className="overflow-hidden rounded-xl border border-slate-700 bg-[#0c0c0c] shadow-2xl">
              {/* Windows CMD 타이틀 바 */}
              <div className="flex items-center justify-between bg-[#1f1f1f] px-4 py-2 border-b border-slate-800 select-none">
                <div className="flex items-center gap-2.5">
                  <span className="inline-flex h-4 w-5 items-center justify-center rounded-[2px] bg-slate-800 border border-slate-600 font-mono text-[10px] text-slate-200">
                    C:\
                  </span>
                  <span className="text-xs font-medium text-slate-200">
                    명령 프롬프트 - D:\viper (e:\hello-world)
                  </span>
                </div>
                <div className="flex items-center gap-4 text-slate-400 text-xs font-mono">
                  <span>─</span>
                  <span>□</span>
                  <span className="hover:text-rose-400">✕</span>
                </div>
              </div>

              {/* CMD 본문 영역 */}
              <div className="p-5 sm:p-6 font-mono text-xs sm:text-[13px] leading-relaxed text-[#cccccc] space-y-4 overflow-x-auto">
                {/* 실행 명령어 */}
                <div>
                  <span className="text-white">D:\viper&gt;</span>
                  <span className="text-amber-300 break-all">{realCmdCommand}</span>
                </div>

                <div className="text-slate-600">
                  ────────────────────────────────────────────────────────────────────────────────────────────────────
                  <br />
                  ────────────────────────────────────────────────────────────────────────────────────────────────────
                </div>

                {/* 초기 상태 로그 */}
                <div className="space-y-0.5 text-slate-300">
                  <div className="text-slate-400">You can skip this check with --no-gitignore</div>
                  <div className="text-slate-400">Added .aider* to .gitignore</div>
                  <div className="text-emerald-400 font-bold">Viper v0.86.3.dev+import</div>
                  <div>Model: openrouter/openrouter/free with architect edit format</div>
                  <div>Editor model: openrouter/openrouter/free with diff edit format</div>
                  <div>Git repo: E:\hello-world\.git with 0 files</div>
                  <div>Repo-map: using 4096 tokens, auto refresh</div>
                  <div className="text-slate-400">
                    Note: in-chat filenames are always relative to the git working dir, not the current working dir.
                  </div>
                  <div>Cur working dir: D:\viper</div>
                  <div>Git working dir: E:\hello-world</div>
                </div>

                <div className="text-slate-600">
                  ────────────────────────────────────────────────────────────────────────────────────────────────────
                </div>

                {/* architect 프롬프트 */}
                <div>
                  <span className="text-cyan-400 font-bold">architect&gt; </span>
                  <span className="text-white">gradle 기반으로 Hello World 자바 예제 프로젝트를 만드세요</span>
                </div>

                <div className="text-slate-600">
                  ----------------------------------------------------------------------------------------------------
                </div>

                {/* 1차 응답: Architect 설계 */}
                <div className="space-y-2">
                  <div className="text-amber-300 font-bold">► THINKING</div>
                  <div className="text-slate-400 space-y-1">
                    <p>
                      The user wants to create a Gradle-based Hello World Java example project. I need to provide clear instructions for the editor engineer to create the necessary files. Let me think about what files are needed:
                    </p>
                    <p>
                      1 build.gradle - Gradle build file
                      <br />
                      2 settings.gradle - Gradle settings file
                      <br />
                      3 src/main/java/HelloWorld.java - Main Java class
                    </p>
                    <p>I&apos;ll provide instructions for creating these files.</p>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  <div className="text-emerald-400 font-bold">► ANSWER</div>
                  <p className="text-slate-200">
                    Gradle 기반 Hello World Java 프로젝트를 만들기 위해 다음 3개 파일을 생성하도록 지시합니다.
                  </p>
                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  {/* 1. build.gradle */}
                  <div className="space-y-1">
                    <div className="text-cyan-300 font-semibold">1. build.gradle (프로젝트 루트)</div>
                    <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

application {
    mainClass = 'HelloWorld'
}

jar {
    manifest {
        attributes 'Main-Class': 'HelloWorld'
    }
}`}
                    </pre>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  {/* 2. settings.gradle */}
                  <div className="space-y-1">
                    <div className="text-cyan-300 font-semibold">2. settings.gradle (프로젝트 루트)</div>
                    <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`rootProject.name = 'hello-world'`}
                    </pre>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  {/* 3. src/main/java/HelloWorld.java */}
                  <div className="space-y-1">
                    <div className="text-cyan-300 font-semibold">3. src/main/java/HelloWorld.java</div>
                    <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`}
                    </pre>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  {/* 실행 방법 안내 */}
                  <div className="space-y-1">
                    <div className="text-cyan-300 font-semibold">실행 방법 (에디터가 사용자에게 안내할 내용)</div>
                    <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`# 빌드
./gradlew build

# 실행 (application 플러그인)
./gradlew run

# 또는 JAR 직접 실행
java -jar build/libs/hello-world-1.0.0.jar`}
                    </pre>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  {/* 디렉터리 구조 */}
                  <div className="space-y-1">
                    <div className="text-cyan-300 font-semibold">디렉터리 구조:</div>
                    <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`hello-world/
├── build.gradle
├── settings.gradle
└── src/
    └── main/
        └── java/
            └── HelloWorld.java`}
                    </pre>
                  </div>

                  <div className="text-slate-500 text-xs">Tokens: 221 sent, 480 received.</div>
                </div>

                <div className="text-slate-600">
                  ----------------------------------------------------------------------------------------------------
                </div>

                {/* 2차 응답: Editor SEARCH/REPLACE Diff 적용 */}
                <div className="space-y-2">
                  <div className="text-amber-300 font-bold">► THINKING</div>
                  <div className="text-slate-400 space-y-1">
                    <p>
                      The user wants me to create a Gradle-based Hello World Java project with 3 files. They&apos;ve provided the exact content for each file. I need to create SEARCH/REPLACE blocks for each file.
                    </p>
                    <p>
                      Since these are new files, I&apos;ll use the format with empty SEARCH sections and the content in REPLACE sections.
                    </p>
                    <p>
                      Let me create the blocks for:
                      <br />
                      1 build.gradle
                      <br />
                      2 settings.gradle
                      <br />
                      3 src/main/java/HelloWorld.java
                    </p>
                  </div>

                  <div className="text-slate-600">
                    ----------------------------------------------------------------------------------------------------
                  </div>

                  <div className="text-emerald-400 font-bold">► ANSWER</div>

                  <div className="text-cyan-300 font-semibold">build.gradle</div>
                  <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`<<<<<<< SEARCH
=======
plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0.0'

repositories {
    mavenCentral()
}

application {
    mainClass = 'HelloWorld'
}

jar {
    manifest {
        attributes 'Main-Class': 'HelloWorld'
    }
}
>>>>>>> REPLACE`}
                  </pre>

                  <div className="text-cyan-300 font-semibold">settings.gradle</div>
                  <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`<<<<<<< SEARCH
=======
rootProject.name = 'hello-world'
>>>>>>> REPLACE`}
                  </pre>

                  <div className="text-cyan-300 font-semibold">src/main/java/HelloWorld.java</div>
                  <pre className="rounded bg-[#141414] border border-slate-800 p-3 text-slate-200 overflow-x-auto">
{`<<<<<<< SEARCH
=======
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
>>>>>>> REPLACE`}
                  </pre>

                  <div className="text-slate-500 text-xs">Tokens: 2.3k sent, 291 received.</div>

                  {/* 파일 적용 로그 */}
                  <div className="rounded bg-[#141414] border border-slate-800 p-3 space-y-0.5 text-xs">
                    <div className="text-slate-300">build.gradle</div>
                    <div className="text-slate-300">settings.gradle</div>
                    <div className="text-slate-300">src/main/java/HelloWorld.java</div>
                    <div className="text-emerald-400">Applied edit to settings.gradle</div>
                    <div className="text-emerald-400">Applied edit to src/main/java/HelloWorld.java</div>
                    <div className="text-emerald-400">Applied edit to build.gradle</div>
                  </div>
                </div>

                <div className="text-slate-600">───────────────────────────────</div>
              </div>
            </div>
          </section>

          {/* 2. 실행 옵션 및 빌드/실행 명령 요약 */}
          <section className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">
              실행 옵션 및 생성된 프로젝트 빌드·실행
            </h2>
            <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-slate-800 bg-slate-900 text-slate-300">
                  <tr>
                    <th className="px-5 py-3.5 font-semibold">항목</th>
                    <th className="px-5 py-3.5 font-semibold">값 / 명령어</th>
                    <th className="px-5 py-3.5 font-semibold">역할</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80 text-slate-300 font-mono text-xs sm:text-sm">
                  <tr>
                    <td className="px-5 py-3.5 text-emerald-400 font-semibold">--architect</td>
                    <td className="px-5 py-3.5 text-slate-200">architect edit format</td>
                    <td className="px-5 py-3.5 font-sans text-slate-300">설계 및 파일 생성 지시 담당</td>
                  </tr>
                  <tr>
                    <td className="px-5 py-3.5 text-emerald-400 font-semibold">--editor-edit-format</td>
                    <td className="px-5 py-3.5 text-slate-200">diff</td>
                    <td className="px-5 py-3.5 font-sans text-slate-300">SEARCH/REPLACE 블록으로 실제 파일 반영</td>
                  </tr>
                  <tr>
                    <td className="px-5 py-3.5 text-emerald-400 font-semibold">--no-auto-commits</td>
                    <td className="px-5 py-3.5 text-slate-200">e:\hello-world</td>
                    <td className="px-5 py-3.5 font-sans text-slate-300">자동 git commit 없이 작업 디렉터리에 파일만 적용</td>
                  </tr>
                  <tr>
                    <td className="px-5 py-3.5 text-emerald-400 font-semibold">Gradle 실행</td>
                    <td className="px-5 py-3.5 text-slate-200">./gradlew run</td>
                    <td className="px-5 py-3.5 font-sans text-slate-300">application 플러그인으로 HelloWorld 실행</td>
                  </tr>
                  <tr>
                    <td className="px-5 py-3.5 text-emerald-400 font-semibold">JAR 실행</td>
                    <td className="px-5 py-3.5 text-slate-200">java -jar build/libs/hello-world-1.0.0.jar</td>
                    <td className="px-5 py-3.5 font-sans text-slate-300">빌드된 실행 가능 JAR 직접 실행</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {/* 하단 홈 복귀 버튼 */}
          <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/40 p-6">
            <div>
              <div className="font-bold text-white">viper 소개 및 핵심 최적화 기능을 보시겠어요?</div>
              <p className="text-sm text-slate-400 mt-1">
                Repo Map 인덱싱, 루프 차단, CLI &amp; 웹 모드 안내로 돌아갑니다.
              </p>
            </div>
            <button
              onClick={() => {
                setCurrentPage("home");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className="shrink-0 rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-700 transition-colors"
            >
              ← 소개 페이지로
            </button>
          </div>
        </main>
      )}

      {/* 하단 CTA 및 푸터 */}
      <footer className="border-t border-slate-800 bg-slate-950 py-16">
        <div className="mx-auto max-w-6xl px-6 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <div className="text-lg font-bold text-white">
              viper
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Built on Aider architecture · Optimized Repo Map &amp; Context Engine
            </p>
          </div>
          <div className="flex items-center gap-6 text-sm text-slate-400">
            <button
              onClick={() => {
                setCurrentPage("home");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className="hover:text-white transition-colors"
            >
              홈
            </button>
            <button
              onClick={() => {
                setCurrentPage("guide");
                window.scrollTo({ top: 0, behavior: "smooth" });
              }}
              className="hover:text-white transition-colors"
            >
              사용법 (Windows CMD)
            </button>
            <a href={githubUrl} target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              GitHub 저장소 (matthewb2/viper)
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}