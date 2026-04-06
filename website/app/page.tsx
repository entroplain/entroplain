export default function Home() {
  const colors = {
    black: '#171717',
    white: '#ffffff',
    gray600: '#4d4d4d',
    gray400: '#808080',
    gray100: '#ebebeb',
    greenAccent: '#22c55e',
    greenLight: '#4ade80',
    shadowBorder: 'rgba(0, 0, 0, 0.08) 0px 0px 0px 1px',
    shadowCard: 'rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 2px, rgba(0,0,0,0.04) 0px 8px 8px -8px, #fafafa 0px 0px 0px 1px',
  }

  return (
    <main style={{ minHeight: '100vh', background: colors.white }}>
      {/* Subtle gradient background */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'radial-gradient(ellipse at top, rgba(34, 197, 94, 0.03) 0%, transparent 50%), radial-gradient(ellipse at bottom right, rgba(59, 130, 246, 0.03) 0%, transparent 50%)',
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      {/* Navigation */}
      <nav style={{
        position: 'sticky',
        top: 0,
        background: 'rgba(255,255,255,0.85)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid #f0f0f0',
        padding: '0 24px',
        height: '64px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        zIndex: 100,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '6px',
            background: `linear-gradient(135deg, ${colors.greenAccent}, ${colors.greenLight})`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}>
            <span style={{ color: 'white', fontWeight: 700, fontSize: '14px' }}>E</span>
          </div>
          <span style={{ fontWeight: 600, fontSize: '16px', letterSpacing: '-0.02em', color: colors.black }}>Entroplain</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
          <a href="#how" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>How it works</a>
          <a href="#features" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>Features</a>
          <a href="https://github.com/entroplain/entroplain" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px', fontWeight: 500 }}>GitHub</a>
          <a href="https://pypi.org/project/entroplain/" style={{
            padding: '8px 16px',
            background: colors.black,
            color: colors.white,
            borderRadius: '6px',
            textDecoration: 'none',
            fontSize: '14px',
            fontWeight: 500,
          }}>Get Started</a>
        </div>
      </nav>

      {/* Hero */}
      <section style={{
        position: 'relative',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '120px 24px 160px',
        textAlign: 'center',
        zIndex: 1,
      }}>
        {/* Badge */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          borderRadius: '9999px',
          background: 'rgba(34, 197, 94, 0.08)',
          marginBottom: '32px',
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: colors.greenAccent }} />
          <span style={{ color: '#15803d', fontSize: '13px', fontWeight: 500 }}>Save 30-50% on API costs</span>
        </div>

        {/* Headline */}
        <h1 style={{
          fontSize: '72px',
          fontWeight: 600,
          letterSpacing: '-0.04em',
          lineHeight: 1.0,
          margin: '0 0 24px 0',
          color: colors.black,
        }}>
          Stop wasting tokens.
        </h1>
        <h1 style={{
          fontSize: '72px',
          fontWeight: 600,
          letterSpacing: '-0.04em',
          lineHeight: 1.0,
          margin: '0 0 32px 0',
          color: colors.gray400,
        }}>
          Exit early when confident.
        </h1>

        {/* Subtitle */}
        <p style={{
          fontSize: '20px',
          color: colors.gray600,
          lineHeight: 1.7,
          maxWidth: '640px',
          margin: '0 auto 48px',
        }}>
          Entroplain monitors LLM reasoning entropy in real-time. When the model 
          confidently knows the answer, it exits — saving tokens without sacrificing quality.
        </p>

        {/* CTAs */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
          <a href="https://pypi.org/project/entroplain/" style={{
            padding: '14px 24px',
            background: colors.greenAccent,
            color: 'white',
            borderRadius: '6px',
            textDecoration: 'none',
            fontSize: '16px',
            fontWeight: 500,
            boxShadow: '0 4px 16px rgba(34, 197, 94, 0.25)',
          }}>
            pip install entroplain
          </a>
          <a href="https://github.com/entroplain/entroplain" style={{
            padding: '14px 24px',
            background: 'transparent',
            color: colors.black,
            borderRadius: '6px',
            textDecoration: 'none',
            fontSize: '16px',
            fontWeight: 500,
            boxShadow: colors.shadowBorder,
          }}>
            View on GitHub
          </a>
        </div>

        {/* Trust indicators */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '48px',
          marginTop: '64px',
          color: colors.gray400,
          fontSize: '14px',
        }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M5 13l4 4L19 7" />
            </svg>
            Works with any LLM
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M5 13l4 4L19 7" />
            </svg>
            Zero code changes
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              <path d="M5 13l4 4L19 7" />
            </svg>
            Real-time dashboard
          </span>
        </div>
      </section>

      {/* Terminal Demo */}
      <section style={{
        position: 'relative',
        maxWidth: '900px',
        margin: '0 auto 160px',
        padding: '0 24px',
        zIndex: 1,
      }}>
        <div style={{
          borderRadius: '12px',
          overflow: 'hidden',
          boxShadow: colors.shadowCard,
        }}>
          {/* Terminal header */}
          <div style={{
            background: '#1a1a1a',
            padding: '14px 16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }} />
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }} />
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27c93f' }} />
            <span style={{ marginLeft: '12px', color: '#666', fontSize: '12px', fontFamily: 'monospace' }}>terminal</span>
          </div>
          {/* Terminal content */}
          <div style={{
            background: '#0a0a0a',
            padding: '32px',
            fontFamily: '"SF Mono", "Fira Code", Consolas, monospace',
            fontSize: '14px',
            lineHeight: 2,
            color: '#a0a0a0',
          }}>
            <div><span style={{ color: '#22c55e' }}>$</span> pip install entroplain</div>
            <div style={{ marginTop: '16px' }}><span style={{ color: '#22c55e' }}>$</span> entroplain-proxy --port 8765 --provider openai</div>
            <div style={{ marginTop: '8px', color: '#666' }}>→ Proxy running on http://localhost:8765</div>
            <div style={{ marginTop: '8px', color: '#666' }}>→ Dashboard at http://localhost:8765/dashboard</div>
            <div style={{ marginTop: '16px' }}><span style={{ color: '#22c55e' }}>$</span> export OPENAI_BASE_URL=http://localhost:8765</div>
            <div style={{ marginTop: '16px', color: '#4ade80' }}>✓ Your agent now exits early when confident</div>
          </div>
        </div>
      </section>

      {/* How it Works - with gradient section */}
      <section id="how" style={{
        position: 'relative',
        background: 'linear-gradient(180deg, #fafafa 0%, #ffffff 100%)',
        padding: '160px 24px',
        zIndex: 1,
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <h2 style={{
            fontSize: '48px',
            fontWeight: 600,
            letterSpacing: '-0.03em',
            textAlign: 'center',
            marginBottom: '80px',
            color: colors.black,
          }}>How it works</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px' }}>
            {[
              { num: '01', title: 'Monitor entropy', desc: 'Track token-level entropy in real-time. Low entropy means high confidence — the model knows the answer.', color: colors.greenAccent },
              { num: '02', title: 'Detect valleys', desc: 'When entropy drops into a sustained valley, the model has converged on a confident, stable answer.', color: '#3b82f6' },
              { num: '03', title: 'Exit early', desc: 'Stop generation once confidence is established. Save 30-50% tokens without quality loss.', color: '#a855f7' },
            ].map((step, i) => (
              <div key={i} style={{
                background: colors.white,
                borderRadius: '12px',
                padding: '40px 32px',
                boxShadow: colors.shadowCard,
                transition: 'transform 0.2s ease, box-shadow 0.2s ease',
              }}>
                <div style={{
                  fontSize: '12px',
                  fontWeight: 600,
                  color: step.color,
                  marginBottom: '16px',
                  fontFamily: 'monospace',
                }}>{step.num}</div>
                <h3 style={{
                  fontSize: '24px',
                  fontWeight: 600,
                  letterSpacing: '-0.02em',
                  marginBottom: '16px',
                  color: colors.black,
                }}>{step.title}</h3>
                <p style={{ color: colors.gray600, lineHeight: 1.7, margin: 0 }}>{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" style={{
        position: 'relative',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '160px 24px',
        zIndex: 1,
      }}>
        <h2 style={{
          fontSize: '48px',
          fontWeight: 600,
          letterSpacing: '-0.03em',
          textAlign: 'center',
          marginBottom: '80px',
          color: colors.black,
        }}>Features</h2>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
          {[
            { title: 'Proxy-based integration', desc: 'Works with any agent — Claude Code, Cursor, OpenAI, any framework. Zero code changes needed.' },
            { title: 'Real-time dashboard', desc: 'Watch entropy visualization live. See exactly when and why early exit triggered.' },
            { title: 'Cost tracking', desc: 'Know exactly how much you saved. Token counts, costs, and savings per request.' },
            { title: 'Multiple exit strategies', desc: 'Valleys, velocity, confidence threshold, repetition detection. Pick your strategy.' },
            { title: 'Multi-provider support', desc: 'OpenAI, Anthropic, NVIDIA, Google Gemini, OpenRouter, local models via Ollama.' },
            { title: 'Python + Node.js', desc: 'Available on PyPI and npm. Use it wherever your agent runs.' },
          ].map((f, i) => (
            <div key={i} style={{
              background: colors.white,
              borderRadius: '12px',
              padding: '32px',
              boxShadow: colors.shadowBorder,
            }}>
              <h3 style={{
                fontSize: '18px',
                fontWeight: 600,
                letterSpacing: '-0.01em',
                marginBottom: '12px',
                color: colors.black,
              }}>{f.title}</h3>
              <p style={{ color: colors.gray600, lineHeight: 1.6, margin: 0, fontSize: '15px' }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Stats - Fixed width for numbers */}
      <section style={{
        position: 'relative',
        background: colors.black,
        padding: '120px 24px',
        zIndex: 1,
      }}>
        <div style={{
          maxWidth: '1000px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '64px',
          textAlign: 'center',
        }}>
          <div>
            <div style={{ fontSize: '80px', fontWeight: 600, letterSpacing: '-0.04em', color: colors.greenLight, marginBottom: '8px', whiteSpace: 'nowrap' }}>50%</div>
            <div style={{ color: colors.gray400, fontSize: '16px' }}>Token savings</div>
          </div>
          <div>
            <div style={{ fontSize: '80px', fontWeight: 600, letterSpacing: '-0.04em', color: 'white', marginBottom: '8px', whiteSpace: 'nowrap' }}>0</div>
            <div style={{ color: colors.gray400, fontSize: '16px' }}>Code changes</div>
          </div>
          <div>
            <div style={{ fontSize: '80px', fontWeight: 600, letterSpacing: '-0.04em', color: 'white', marginBottom: '8px', whiteSpace: 'nowrap' }}>6+</div>
            <div style={{ color: colors.gray400, fontSize: '16px' }}>LLM providers</div>
          </div>
        </div>
      </section>

      {/* Supported Providers */}
      <section style={{
        position: 'relative',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '120px 24px',
        textAlign: 'center',
        zIndex: 1,
      }}>
        <h3 style={{
          fontSize: '14px',
          fontWeight: 500,
          color: colors.gray400,
          marginBottom: '32px',
          textTransform: 'uppercase',
          letterSpacing: '0.1em',
        }}>Works with any provider that exposes logprobs</h3>
        
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '12px',
        }}>
          {['OpenAI', 'Anthropic Claude', 'NVIDIA NIM', 'Google Gemini', 'OpenRouter', 'Ollama', 'Together AI', 'Groq'].map((p) => (
            <div key={p} style={{
              padding: '10px 20px',
              background: '#fafafa',
              borderRadius: '6px',
              boxShadow: colors.shadowBorder,
              color: colors.gray600,
              fontSize: '14px',
              fontWeight: 500,
            }}>{p}</div>
          ))}
        </div>
      </section>

      {/* Final CTA */}
      <section style={{
        position: 'relative',
        maxWidth: '900px',
        margin: '0 auto 120px',
        padding: '0 24px',
        zIndex: 1,
      }}>
        <div style={{
          background: `linear-gradient(135deg, ${colors.greenAccent}, ${colors.greenLight})`,
          borderRadius: '24px',
          padding: '80px 64px',
          textAlign: 'center',
        }}>
          <h2 style={{
            fontSize: '40px',
            fontWeight: 600,
            letterSpacing: '-0.03em',
            color: 'white',
            marginBottom: '16px',
          }}>Start saving tokens today</h2>
          <p style={{
            color: 'rgba(255,255,255,0.85)',
            marginBottom: '32px',
            fontSize: '18px',
          }}>
            Install in 30 seconds. No code changes. Works with your existing agent setup.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
            <a href="https://pypi.org/project/entroplain/" style={{
              padding: '16px 32px',
              background: 'white',
              color: colors.greenAccent,
              borderRadius: '6px',
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 600,
            }}>pip install entroplain</a>
            <a href="https://github.com/entroplain/entroplain" style={{
              padding: '16px 32px',
              background: 'rgba(255,255,255,0.15)',
              color: 'white',
              borderRadius: '6px',
              textDecoration: 'none',
              fontSize: '16px',
              fontWeight: 500,
            }}>View on GitHub</a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        position: 'relative',
        borderTop: '1px solid #ebebeb',
        padding: '48px 24px',
        zIndex: 1,
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{
              width: '24px',
              height: '24px',
              borderRadius: '4px',
              background: `linear-gradient(135deg, ${colors.greenAccent}, ${colors.greenLight})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <span style={{ color: 'white', fontWeight: 700, fontSize: '11px' }}>E</span>
            </div>
            <span style={{ fontWeight: 500, fontSize: '14px', color: colors.black }}>Entroplain</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '32px' }}>
            <a href="https://github.com/entroplain/entroplain" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px' }}>GitHub</a>
            <a href="https://pypi.org/project/entroplain/" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px' }}>PyPI</a>
            <a href="https://www.npmjs.com/package/entroplain" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px' }}>npm</a>
            <a href="https://github.com/entroplain/entroplain/blob/main/LICENSE" style={{ color: colors.gray600, textDecoration: 'none', fontSize: '14px' }}>MIT License</a>
          </div>
        </div>
      </footer>
    </main>
  )
}
