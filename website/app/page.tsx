"use client";

import React, { useEffect, useState } from "react";


export default function ViperLandingPage() {
  const [activeMode, setActiveMode] = useState<"cli" | "web">("cli");
  const [copied, setCopied] = useState(false);

  const githubUrl = "https://github.com/matthewb2/viper";
  const installCommand = "pip install git+https://github.com/matthewb2/viper.git";

  const handleCopy = () => {
    navigator.clipboard.writeText(installCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
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
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-mono font-bold">
              &gt;_
            </div>
            <span className="text-lg font-bold tracking-tight text-white">
              viper
            </span>
            <span className="ml-2 rounded-full bg-slate-800 px-2.5 py-0.5 text-xs font-medium text-slate-400 border border-slate-700">
              Aider Fork
            </span>
          </div>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <a href="#features" className="hover:text-white transition-colors">
              핵심 최적화
            </a>
            <a href="#architecture" className="hover:text-white transition-colors">
              동작 원리
            </a>
            <a href="#modes" className="hover:text-white transition-colors">
              CLI &amp; 웹 모드
            </a>
            <a href="#benchmark" className="hover:text-white transition-colors">
              성능 개선
            </a>
          </nav>

          <div className="flex items-center gap-3">
            <a
              href={githubUrl}
              target="_blank"
              rel="noreferrer"
              className="rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-800 transition-colors"
            >
              GitHub
            </a>
            <a
              href="#quickstart"
              className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 transition-colors"
            >
              시작하기
            </a>
          </div>
        </div>
      </header>

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
                onClick={handleCopy}
                className="ml-3 shrink-0 rounded-lg bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-200 hover:bg-slate-700 transition-colors border border-slate-700"
              >
                {copied ? "복사 완료!" : "명령어 복사"}
              </button>
            </div>
            <div className="mt-4 flex items-center justify-center gap-4 text-xs text-slate-400">
              <span>Gemini · OpenAI · Claude · DeepSeek · Groq · Ollama 지원</span>
              <span>·</span>
              <a
                href={githubUrl}
                target="_blank"
                rel="noreferrer"
                className="text-emerald-400 hover:underline font-medium"
              >
                소스코드 보기 →
              </a>
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
            {/* 카드 1 */}
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

            {/* 카드 2 */}
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

            {/* 카드 3 */}
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

            {/* 모드 전환 탭 */}
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

          {/* 프리뷰 윈도우 */}
          <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 shadow-2xl">
            {/* 윈도우 타이틀 바 */}
            <div className="flex items-center justify-between border-b border-slate-800 bg-slate-900/90 px-4 py-3">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded-full bg-rose-500/80" />
                <span className="h-3 w-3 rounded-full bg-amber-500/80" />
                <span className="h-3 w-3 rounded-full bg-emerald-500/80" />
              </div>
              <span className="font-mono text-xs text-slate-400">
                {activeMode === "cli"
                  ? "bash — viper --model gemini/gemini-2.5-pro"
                  : "http://localhost:8501 — viper Web Workspace"}
              </span>
              <div className="w-12" />
            </div>

            {/* 탭 내용 */}
            {activeMode === "cli" ? (
              <div className="p-6 font-mono text-xs sm:text-sm leading-relaxed space-y-3 text-slate-300">
                <p className="text-emerald-400">
                  $ viper --api-key $LLM_API_KEY
                </p>
                <p className="text-slate-500">
                  [RepoMap] 142개 파일 인덱싱 완료 (0.38s) → 핵심 연관 파일 4개 자동 선택됨
                </p>
                <p className="text-slate-400">
                  &nbsp;&nbsp;• src/core/parser.ts (Score: 0.94)
                  <br />
                  &nbsp;&nbsp;• src/core/context_ranker.ts (Score: 0.89)
                </p>
                <p className="text-cyan-300 pt-2">
                  &gt; 비동기 스트림 처리 시 메모리 누수가 발생하는 부분을 수정하고 테스트 코드를 추가해줘.
                </p>
                <p className="text-slate-300 pt-1">
                  [viper] 문맥 분석 완료. 루프 가드 활성화됨. 1회차 패치 적용 중...
                </p>
                <div className="rounded-lg bg-slate-900 border border-slate-800 p-3 text-xs">
                  <span className="text-emerald-400">+ Applied diff to src/core/parser.ts (+18, -4)</span>
                  <br />
                  <span className="text-emerald-400">+ Created tests/parser_stream.test.ts</span>
                  <br />
                  <span className="text-slate-400">✓ Lint &amp; Typecheck passed on 1st attempt.</span>
                </div>
              </div>
            ) : (
              <div className="grid md:grid-cols-3 min-h-[300px]">
                {/* 좌측 사이드바 */}
                <div className="border-b md:border-b-0 md:border-r border-slate-800 bg-slate-900/40 p-5 space-y-4">
                  <div className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    선택된 문맥 파일 (Auto)
                  </div>
                  <ul className="space-y-2 text-xs font-mono">
                    <li className="flex items-center justify-between rounded bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1.5 text-emerald-300">
                      <span>src/core/parser.ts</span>
                      <span>94%</span>
                    </li>
                    <li className="flex items-center justify-between rounded bg-slate-900 px-2.5 py-1.5 text-slate-300">
                      <span>src/api/client.ts</span>
                      <span>81%</span>
                    </li>
                    <li className="flex items-center justify-between rounded bg-slate-900 px-2.5 py-1.5 text-slate-400">
                      <span>src/types/index.ts</span>
                      <span>67%</span>
                    </li>
                  </ul>
                  <div className="pt-2 border-t border-slate-800 text-xs text-slate-400">
                    실행 명령: <code className="text-emerald-400">viper --browser</code>
                  </div>
                </div>

                {/* 우측 코드 Diff 뷰 */}
                <div className="md:col-span-2 p-6 font-mono text-xs space-y-3">
                  <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800">
                    <span>실시간 Diff 리뷰 &amp; 원클릭 커밋</span>
                    <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-emerald-300">
                      토큰 62% 절감
                    </span>
                  </div>
                  <pre className="overflow-x-auto text-slate-300 leading-relaxed">
{`  async function* readStream(reader: ReadableStreamDefaultReader) {
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        yield value;
      }
+   } finally {
+     reader.releaseLock();
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
            <a href="#features" className="hover:text-white transition-colors">
              특징
            </a>
            <a href="#modes" className="hover:text-white transition-colors">
              사용 모드
            </a>
            <a href={githubUrl} target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              GitHub 저장소 (matthewb2/viper)
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}