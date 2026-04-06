export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Hero */}
      <section className="max-w-5xl mx-auto px-6 pt-24 pb-16">
        <nav className="flex items-center justify-between mb-20">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
              <span className="text-white font-bold text-sm">E</span>
            </div>
            <span className="font-semibold text-lg tracking-tight">Entroplain</span>
          </div>
          <div className="flex items-center gap-6 text-sm">
            <a href="#how-it-works" className="text-gray-600 hover:text-gray-900 transition">How it works</a>
            <a href="#features" className="text-gray-600 hover:text-gray-900 transition">Features</a>
            <a href="https://github.com/entroplain/entroplain" className="text-gray-600 hover:text-gray-900 transition">GitHub</a>
            <a href="https://pypi.org/project/entroplain/" className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-medium">
              Get Started
            </a>
          </div>
        </nav>

        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-green-50 text-green-700 text-sm font-medium mb-6">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Save 30-50% on API costs
          </div>
          
          <h1 className="text-5xl font-semibold tracking-tight mb-6 leading-tight">
            Stop wasting tokens.<br/>
            <span className="text-gray-400">Exit early when confident.</span>
          </h1>
          
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Entroplain monitors LLM reasoning entropy in real-time. When the model 
            confidently knows the answer, it exits — saving tokens without sacrificing quality.
          </p>

          <div className="flex items-center justify-center gap-4">
            <a href="https://pypi.org/project/entroplain/" className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition font-medium text-lg">
              pip install entroplain
            </a>
            <a href="https://github.com/entroplain/entroplain" className="px-6 py-3 border border-gray-200 rounded-lg hover:border-gray-300 transition font-medium text-lg">
              View on GitHub
            </a>
          </div>

          <div className="mt-12 flex items-center justify-center gap-8 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Works with any LLM
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Zero code changes
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Real-time dashboard
            </div>
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section className="max-w-5xl mx-auto px-6 py-16">
        <div className="rounded-xl overflow-hidden card-shadow">
          <div className="bg-gray-900 px-4 py-3 flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="ml-2 text-gray-400 text-sm">terminal</span>
          </div>
          <pre className="p-6 text-sm leading-relaxed">
            <code>{`# Install
$ pip install entroplain

# Run the proxy (works with any agent)
$ entroplain-proxy --port 8765 --provider openai

# Set your agent's API endpoint
$ export OPENAI_BASE_URL=http://localhost:8765

# That's it. Your agent now exits early when confident.
# Open http://localhost:8765/dashboard to watch entropy in real-time.`}</code>
          </pre>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" className="max-w-5xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-semibold tracking-tight mb-12 text-center">How it works</h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="p-6 rounded-xl border-shadow">
            <div className="w-12 h-12 rounded-lg bg-green-50 flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Monitor entropy</h3>
            <p className="text-gray-600">
              Track token-level entropy in real-time. Low entropy = high confidence = the model knows the answer.
            </p>
          </div>

          <div className="p-6 rounded-xl border-shadow">
            <div className="w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center mb-4">
              <span className="text-2xl">🏔️</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Detect valleys</h3>
            <p className="text-gray-600">
              When entropy drops into a sustained valley, the model has converged on a confident answer.
            </p>
          </div>

          <div className="p-6 rounded-xl border-shadow">
            <div className="w-12 h-12 rounded-lg bg-purple-50 flex items-center justify-center mb-4">
              <span className="text-2xl">✂️</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Exit early</h3>
            <p className="text-gray-600">
              Stop generation once confidence is established. Save 30-50% tokens without quality loss.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="max-w-5xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-semibold tracking-tight mb-12 text-center">Features</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">🔄 Proxy-based integration</h3>
            <p className="text-gray-600 text-sm">Works with any agent — Claude Code, Cursor, OpenAI, you name it. No code changes needed.</p>
          </div>
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">📈 Real-time dashboard</h3>
            <p className="text-gray-600 text-sm">Watch entropy visualization live. See exactly when and why early exit triggered.</p>
          </div>
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">💰 Cost tracking</h3>
            <p className="text-gray-600 text-sm">Know exactly how much you saved. Token counts, costs, and savings per request.</p>
          </div>
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">🎯 Multiple exit strategies</h3>
            <p className="text-gray-600 text-sm">Valleys, velocity, confidence threshold, repetition detection. Pick what works for your use case.</p>
          </div>
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">🔌 Multi-provider support</h3>
            <p className="text-gray-600 text-sm">OpenAI, Anthropic, NVIDIA, Google Gemini, OpenRouter, local models via Ollama.</p>
          </div>
          <div className="p-6 rounded-xl border-shadow">
            <h3 className="font-semibold mb-2">📦 Python + Node.js</h3>
            <p className="text-gray-600 text-sm">Available on PyPI and npm. Use it wherever your agent runs.</p>
          </div>
        </div>
      </section>

      {/* Supported Providers */}
      <section className="max-w-5xl mx-auto px-6 py-16">
        <h2 className="text-3xl font-semibold tracking-tight mb-8 text-center">Supported Providers</h2>
        <p className="text-gray-600 text-center mb-12">Works with any provider that exposes logprobs</p>
        
        <div className="flex flex-wrap justify-center gap-4">
          {['OpenAI', 'Anthropic Claude', 'NVIDIA NIM', 'Google Gemini', 'OpenRouter', 'Ollama', 'Together AI', 'Groq'].map((provider) => (
            <div key={provider} className="px-4 py-2 rounded-lg bg-gray-50 text-gray-700 text-sm font-medium">
              {provider}
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section className="max-w-5xl mx-auto px-6 py-16">
        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-5xl font-bold text-green-500 mb-2">30-50%</div>
            <div className="text-gray-600">Token savings</div>
          </div>
          <div>
            <div className="text-5xl font-bold text-gray-900 mb-2">0</div>
            <div className="text-gray-600">Code changes needed</div>
          </div>
          <div>
            <div className="text-5xl font-bold text-gray-900 mb-2">58</div>
            <div className="text-gray-600">Design systems available</div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-5xl mx-auto px-6 py-16 text-center">
        <div className="rounded-2xl bg-gray-900 text-white p-12">
          <h2 className="text-3xl font-semibold mb-4">Start saving tokens today</h2>
          <p className="text-gray-400 mb-8 max-w-xl mx-auto">
            Install in 30 seconds. No code changes. Works with your existing agent setup.
          </p>
          <div className="flex items-center justify-center gap-4">
            <a href="https://pypi.org/project/entroplain/" className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition font-medium">
              pip install entroplain
            </a>
            <a href="https://github.com/entroplain/entroplain" className="px-6 py-3 border border-gray-700 rounded-lg hover:border-gray-600 transition font-medium">
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="max-w-5xl mx-auto px-6 py-12 border-t border-gray-100">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
              <span className="text-white font-bold text-xs">E</span>
            </div>
            <span className="font-medium text-sm">Entroplain</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-gray-500">
            <a href="https://github.com/entroplain/entroplain" className="hover:text-gray-900 transition">GitHub</a>
            <a href="https://pypi.org/project/entroplain/" className="hover:text-gray-900 transition">PyPI</a>
            <a href="https://www.npmjs.com/package/entroplain" className="hover:text-gray-900 transition">npm</a>
            <a href="https://github.com/entroplain/entroplain/blob/main/LICENSE" className="hover:text-gray-900 transition">MIT License</a>
          </div>
        </div>
      </footer>
    </main>
  )
}
