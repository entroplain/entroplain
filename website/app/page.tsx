export default function Home() {
  return (
    <main style={{ minHeight: '100vh', fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif' }}>
      {/* Hero */}
      <section style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px', paddingTop: '80px' }}>
        <nav style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '80px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ 
              width: '32px', 
              height: '32px', 
              borderRadius: '8px', 
              background: 'linear-gradient(135deg, #4ade80, #22c55e)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <span style={{ color: 'white', fontWeight: 700, fontSize: '16px' }}>E</span>
            </div>
            <span style={{ fontWeight: 600, fontSize: '18px', letterSpacing: '-0.02em' }}>Entroplain</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
            <a href="#how-it-works" style={{ color: '#666', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>How it works</a>
            <a href="#features" style={{ color: '#666', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>Features</a>
            <a href="https://github.com/entroplain/entroplain" style={{ color: '#666', textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>GitHub</a>
            <a href="https://pypi.org/project/entroplain/" style={{ 
              padding: '8px 16px', 
              background: '#171717', 
              color: 'white', 
              borderRadius: '8px', 
              textDecoration: 'none',
              fontSize: '14px',
              fontWeight: 500
            }}>Get Started</a>
          </div>
        </nav>

        <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
          <div style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            gap: '8px', 
            padding: '6px 12px', 
            borderRadius: '100px', 
              background: 'rgba(74, 222, 128, 0.1)', 
            color: '#16a34a',
            fontSize: '14px',
            fontWeight: 500,
            marginBottom: '24px'
          }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#22c55e' }}></span>
            Save 30-50% on API costs
          </div>
          
          <h1 style={{ 
            fontSize: '56px', 
            fontWeight: 600, 
            letterSpacing: '-0.03em', 
            lineHeight: 1.1,
            marginBottom: '24px',
            color: '#171717'
          }}>
            Stop wasting tokens.
            <br />
            <span style={{ color: '#999' }}>Exit early when confident.</span>
          </h1>
          
          <p style={{ 
            fontSize: '20px', 
            color: '#666', 
            lineHeight: 1.6,
            marginBottom: '32px',
            maxWidth: '600px',
            margin: '0 auto 32px auto'
          }}>
            Entroplain monitors LLM reasoning entropy in real-time. When the model 
            confidently knows the answer, it exits — saving tokens without sacrificing quality.
          </p>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px', marginBottom: '48px' }}>
            <a href="https://pypi.org/project/entroplain/" style={{ 
              padding: '14px 28px', 
              background: '#22c55e', 
              color: 'white', 
              borderRadius: '10px', 
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 600,
              boxShadow: '0 4px 12px rgba(34, 197, 94, 0.3)'
            }}>
              pip install entroplain
            </a>
            <a href="https://github.com/entroplain/entroplain" style={{ 
              padding: '14px 28px', 
              border: '1px solid #e5e5e5', 
              borderRadius: '10px', 
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 500,
              color: '#171717'
            }}>
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section style={{ maxWidth: '900px', margin: '60px auto', padding: '0 24px' }}>
        <div style={{ 
          borderRadius: '16px', 
          overflow: 'hidden',
          boxShadow: '0 4px 24px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.05)'
        }}>
          <div style={{ 
            background: '#1a1a1a', 
            padding: '12px 16px', 
            display: 'flex', 
            alignItems: 'center', 
            gap: '8px' 
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }}></div>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27c93f' }}></div>
            <span style={{ marginLeft: '12px', color: '#666', fontSize: '13px' }}>terminal</span>
          </div>
          <pre style={{ 
            background: '#1a1a1a', 
            padding: '24px', 
            margin: 0,
            fontFamily: '"SF Mono", "Fira Code", monospace',
            fontSize: '14px',
            lineHeight: 1.6,
            color: '#e0e0e0',
            overflow: 'auto'
          }}>{`# Install
$ pip install entroplain

# Run the proxy (works with any agent)
$ entroplain-proxy --port 8765 --provider openai

# That's it. Your agent now exits early when confident.
# Open http://localhost:8765/dashboard to watch entropy in real-time.`}</pre>
        </div>
      </section>

      {/* How it Works */}
      <section id="how-it-works" style={{ maxWidth: '1200px', margin: '80px auto', padding: '0 24px' }}>
        <h2 style={{ 
          fontSize: '36px', 
          fontWeight: 600, 
          textAlign: 'center', 
          marginBottom: '48px',
          letterSpacing: '-0.02em'
        }}>How it works</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px' }}>
          <div style={{ 
            padding: '32px', 
            borderRadius: '16px',
            background: '#fafafa',
            border: '1px solid #eee'
          }}>
            <div style={{ 
              width: '56px', 
              height: '56px', 
              borderRadius: '12px', 
              background: 'rgba(74, 222, 128, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              fontSize: '28px'
            }}>📊</div>
            <h3 style={{ fontWeight: 600, fontSize: '20px', marginBottom: '12px', letterSpacing: '-0.01em' }}>Monitor entropy</h3>
            <p style={{ color: '#666', lineHeight: 1.6, margin: 0 }}>
              Track token-level entropy in real-time. Low entropy = high confidence.
            </p>
          </div>

          <div style={{ 
            padding: '32px', 
            borderRadius: '16px',
            background: '#fafafa',
            border: '1px solid #eee'
          }}>
            <div style={{ 
              width: '56px', 
              height: '56px', 
              borderRadius: '12px', 
              background: 'rgba(59, 130, 246, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              fontSize: '28px'
            }}>🏔️</div>
            <h3 style={{ fontWeight: 600, fontSize: '20px', marginBottom: '12px', letterSpacing: '-0.01em' }}>Detect valleys</h3>
            <p style={{ color: '#666', lineHeight: 1.6, margin: 0 }}>
              When entropy drops into a sustained valley, the model has converged.
            </p>
          </div>

          <div style={{ 
            padding: '32px', 
            borderRadius: '16px',
            background: '#fafafa',
            border: '1px solid #eee'
          }}>
            <div style={{ 
              width: '56px', 
              height: '56px', 
              borderRadius: '12px', 
              background: 'rgba(168, 85, 247, 0.1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              fontSize: '28px'
            }}>✂️</div>
            <h3 style={{ fontWeight: 600, fontSize: '20px', marginBottom: '12px', letterSpacing: '-0.01em' }}>Exit early</h3>
            <p style={{ color: '#666', lineHeight: 1.6, margin: 0 }}>
              Stop generation once confident. Save 30-50% tokens.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" style={{ maxWidth: '1200px', margin: '80px auto', padding: '0 24px' }}>
        <h2 style={{ 
          fontSize: '36px', 
          fontWeight: 600, 
          textAlign: 'center', 
          marginBottom: '48px',
          letterSpacing: '-0.02em'
        }}>Features</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
          {[
            { icon: '🔄', title: 'Proxy-based integration', desc: 'Works with any agent — Claude Code, Cursor, OpenAI. No code changes.' },
            { icon: '📈', title: 'Real-time dashboard', desc: 'Watch entropy visualization live. See when and why early exit triggered.' },
            { icon: '💰', title: 'Cost tracking', desc: 'Know exactly how much you saved. Token counts and costs per request.' },
            { icon: '🎯', title: 'Multiple exit strategies', desc: 'Valleys, velocity, confidence threshold, repetition detection.' },
            { icon: '🔌', title: 'Multi-provider support', desc: 'OpenAI, Anthropic, NVIDIA, Google Gemini, OpenRouter, Ollama.' },
            { icon: '📦', title: 'Python + Node.js', desc: 'Available on PyPI and npm. Use it wherever your agent runs.' },
          ].map((f, i) => (
            <div key={i} style={{ 
              padding: '24px', 
              borderRadius: '12px',
              border: '1px solid #eee',
              display: 'flex',
              gap: '16px',
              alignItems: 'flex-start'
            }}>
              <span style={{ fontSize: '24px' }}>{f.icon}</span>
              <div>
                <h3 style={{ fontWeight: 600, fontSize: '16px', marginBottom: '8px', letterSpacing: '-0.01em' }}>{f.title}</h3>
                <p style={{ color: '#666', fontSize: '14px', lineHeight: 1.5, margin: 0 }}>{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Stats */}
      <section style={{ maxWidth: '1000px', margin: '100px auto', padding: '0 24px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '48px', textAlign: 'center' }}>
          <div>
            <div style={{ fontSize: '64px', fontWeight: 700, color: '#22c55e', marginBottom: '8px' }}>30-50%</div>
            <div style={{ color: '#666', fontSize: '18px' }}>Token savings</div>
          </div>
          <div>
            <div style={{ fontSize: '64px', fontWeight: 700, color: '#171717', marginBottom: '8px' }}>0</div>
            <div style={{ color: '#666', fontSize: '18px' }}>Code changes needed</div>
          </div>
          <div>
            <div style={{ fontSize: '64px', fontWeight: 700, color: '#171717', marginBottom: '8px' }}>6+</div>
            <div style={{ color: '#666', fontSize: '18px' }}>LLM providers</div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section style={{ maxWidth: '900px', margin: '80px auto', padding: '0 24px' }}>
        <div style={{ 
          borderRadius: '24px', 
          background: '#171717', 
          padding: '64px 48px', 
          textAlign: 'center' 
        }}>
          <h2 style={{ color: 'white', fontSize: '32px', fontWeight: 600, marginBottom: '16px', letterSpacing: '-0.02em' }}>
            Start saving tokens today
          </h2>
          <p style={{ color: '#999', marginBottom: '32px', fontSize: '18px' }}>
            Install in 30 seconds. No code changes. Works with your existing setup.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
            <a href="https://pypi.org/project/entroplain/" style={{ 
              padding: '14px 28px', 
              background: '#22c55e', 
              color: 'white', 
              borderRadius: '10px', 
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 600
            }}>
              pip install entroplain
            </a>
            <a href="https://github.com/entroplain/entroplain" style={{ 
              padding: '14px 28px', 
              border: '1px solid #333', 
              borderRadius: '10px', 
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 500,
              color: 'white'
            }}>
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ 
        maxWidth: '1200px', 
        margin: '0 auto', 
        padding: '48px 24px', 
        borderTop: '1px solid #eee',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ 
            width: '24px', 
            height: '24px', 
            borderRadius: '6px', 
            background: 'linear-gradient(135deg, #4ade80, #22c55e)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <span style={{ color: 'white', fontWeight: 700, fontSize: '12px' }}>E</span>
          </div>
          <span style={{ fontWeight: 500, fontSize: '14px' }}>Entroplain</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
          <a href="https://github.com/entroplain/entroplain" style={{ color: '#666', textDecoration: 'none', fontSize: '14px' }}>GitHub</a>
          <a href="https://pypi.org/project/entroplain/" style={{ color: '#666', textDecoration: 'none', fontSize: '14px' }}>PyPI</a>
          <a href="https://www.npmjs.com/package/entroplain" style={{ color: '#666', textDecoration: 'none', fontSize: '14px' }}>npm</a>
          <a href="https://github.com/entroplain/entroplain/blob/main/LICENSE" style={{ color: '#666', textDecoration: 'none', fontSize: '14px' }}>MIT License</a>
        </div>
      </footer>
    </main>
  )
}
