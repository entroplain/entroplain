export default function Home() {
  // Inspired by Vercel + Linear + Stripe design systems
  const colors = {
    // Vercel-inspired near-black (not pure black)
    black: '#171717',
    white: '#ffffff',
    
    // Linear-inspired dark surfaces
    darkBg: '#0a0a0a',
    darkSurface: '#111111',
    
    // Stripe-inspired deep navy for headings
    navy: '#0a1628',
    
    // Text hierarchy (Linear-style)
    textPrimary: '#f7f8f8',
    textSecondary: '#a0a0a0',
    textMuted: '#666666',
    
    // Brand accent - keeping green for Entroplain
    accent: '#22c55e',
    accentLight: '#4ade80',
    accentDark: '#16a34a',
    accentGlow: 'rgba(34, 197, 94, 0.15)',
    
    // Stripe-inspired blue-tinted shadows
    shadowBlue: 'rgba(50, 50, 93, 0.15)',
    shadowAmbient: 'rgba(0, 0, 0, 0.08)',
    
    // Vercel shadow-as-border
    shadowBorder: 'rgba(0, 0, 0, 0.06) 0px 0px 0px 1px',
    shadowCard: 'rgba(50, 50, 93, 0.12) 0px 8px 24px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px',
    shadowCardHover: 'rgba(50, 50, 93, 0.18) 0px 12px 40px, rgba(0, 0, 0, 0.12) 0px 0px 0px 1px',
    
    // Linear-style borders
    borderSubtle: 'rgba(255, 255, 255, 0.06)',
    borderLight: 'rgba(0, 0, 0, 0.06)',
  }

  return (
    <main style={{ minHeight: '100vh', background: colors.darkBg, color: colors.textPrimary, fontFamily: 'Inter, -apple-system, system-ui, sans-serif' }}>
      {/* Ambient gradient background - inspired by Linear */}
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: `
          radial-gradient(ellipse 80% 50% at 50% -20%, rgba(34, 197, 94, 0.15), transparent),
          radial-gradient(ellipse 60% 40% at 100% 0%, rgba(59, 130, 246, 0.08), transparent),
          radial-gradient(ellipse 50% 30% at 0% 100%, rgba(168, 85, 247, 0.05), transparent)
        `,
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      {/* Navigation - Linear-inspired sticky */}
      <nav style={{
        position: 'sticky',
        top: 0,
        background: 'rgba(10, 10, 10, 0.8)',
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${colors.borderSubtle}`,
        padding: '0 24px',
        height: '72px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        zIndex: 100,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            background: `linear-gradient(135deg, ${colors.accent}, ${colors.accentLight})`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: `0 4px 12px rgba(34, 197, 94, 0.3)`,
          }}>
            <span style={{ color: 'white', fontWeight: 700, fontSize: '16px' }}>E</span>
          </div>
          <span style={{ fontWeight: 600, fontSize: '18px', letterSpacing: '-0.03em' }}>Entroplain</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '40px' }}>
          <a href="#how" style={{ color: colors.textSecondary, textDecoration: 'none', fontSize: '15px', fontWeight: 500, transition: 'color 0.2s' }}>How it works</a>
          <a href="#features" style={{ color: colors.textSecondary, textDecoration: 'none', fontSize: '15px', fontWeight: 500, transition: 'color 0.2s' }}>Features</a>
          <a href="https://github.com/entroplain/entroplain" style={{ color: colors.textSecondary, textDecoration: 'none', fontSize: '15px', fontWeight: 500, transition: 'color 0.2s' }}>GitHub</a>
          <a href="https://pypi.org/project/entroplain/" style={{
            padding: '10px 20px',
            background: colors.accent,
            color: 'white',
            borderRadius: '8px',
            textDecoration: 'none',
            fontSize: '15px',
            fontWeight: 600,
            transition: 'all 0.2s',
            boxShadow: `0 4px 12px rgba(34, 197, 94, 0.25)`,
          }}>Get Started</a>
        </div>
      </nav>

      {/* Hero - Stripe-inspired light headlines */}
      <section style={{
        position: 'relative',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '140px 24px 180px',
        textAlign: 'center',
        zIndex: 1,
      }}>
        {/* Badge - Linear-style pill */}
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '8px 16px',
          borderRadius: '100px',
          background: colors.accentGlow,
          border: `1px solid rgba(34, 197, 94, 0.2)`,
          marginBottom: '40px',
        }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: colors.accent, boxShadow: `0 0 8px ${colors.accent}` }} />
          <span style={{ color: colors.accentLight, fontSize: '14px', fontWeight: 500, letterSpacing: '0.02em' }}>Save up to 50% on API costs</span>
        </div>

        {/* Headline - Stripe weight 300 + Vercel tight tracking */}
        <h1 style={{
          fontSize: '80px',
          fontWeight: 300,
          letterSpacing: '-0.05em',
          lineHeight: 1.0,
          margin: '0 0 16px 0',
          color: colors.textPrimary,
        }}>
          Stop wasting tokens.
        </h1>
        <h1 style={{
          fontSize: '80px',
          fontWeight: 300,
          letterSpacing: '-0.05em',
          lineHeight: 1.0,
          margin: '0 0 48px 0',
          background: `linear-gradient(135deg, ${colors.textSecondary}, ${colors.textMuted})`,
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}>
          Exit early when confident.
        </h1>

        {/* Subtitle */}
        <p style={{
          fontSize: '22px',
          fontWeight: 400,
          color: colors.textSecondary,
          lineHeight: 1.6,
          maxWidth: '680px',
          margin: '0 auto 56px',
        }}>
          Entroplain monitors LLM reasoning entropy in real-time. When the model 
          confidently knows the answer, it exits — saving tokens without sacrificing quality.
        </p>

        {/* CTAs */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
          <a href="https://pypi.org/project/entroplain/" style={{
            padding: '18px 36px',
            background: colors.accent,
            color: 'white',
            borderRadius: '10px',
            textDecoration: 'none',
            fontSize: '17px',
            fontWeight: 600,
            boxShadow: `0 8px 24px rgba(34, 197, 94, 0.35)`,
            transition: 'all 0.2s',
          }}>
            pip install entroplain
          </a>
          <a href="https://github.com/entroplain/entroplain" style={{
            padding: '18px 36px',
            background: 'rgba(255, 255, 255, 0.04)',
            color: colors.textPrimary,
            borderRadius: '10px',
            textDecoration: 'none',
            fontSize: '17px',
            fontWeight: 500,
            border: `1px solid ${colors.borderSubtle}`,
            transition: 'all 0.2s',
          }}>
            View on GitHub
          </a>
        </div>

        {/* Trust indicators - Linear-style */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '56px',
          marginTop: '80px',
          color: colors.textMuted,
          fontSize: '15px',
        }}>
          {['Works with any LLM', 'Zero code changes', 'Real-time dashboard'].map((text, i) => (
            <span key={i} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <svg width="18" height="18" fill="none" stroke={colors.accent} strokeWidth="2.5" viewBox="0 0 24 24">
                <path d="M5 13l4 4L19 7" />
              </svg>
              {text}
            </span>
          ))}
        </div>
      </section>

      {/* Terminal Demo - Linear-inspired */}
      <section style={{
        position: 'relative',
        maxWidth: '960px',
        margin: '0 auto 180px',
        padding: '0 24px',
        zIndex: 1,
      }}>
        <div style={{
          borderRadius: '16px',
          overflow: 'hidden',
          background: colors.darkSurface,
          boxShadow: colors.shadowCard,
          border: `1px solid ${colors.borderSubtle}`,
        }}>
          {/* Terminal header */}
          <div style={{
            padding: '16px 20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            borderBottom: `1px solid ${colors.borderSubtle}`,
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }} />
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }} />
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27c93f' }} />
            <span style={{ marginLeft: '16px', color: colors.textMuted, fontSize: '13px', fontFamily: 'monospace' }}>terminal</span>
          </div>
          {/* Terminal content */}
          <div style={{
            padding: '32px',
            fontFamily: '"SF Mono", "Fira Code", Consolas, monospace',
            fontSize: '15px',
            lineHeight: 2,
            color: colors.textSecondary,
          }}>
            <div><span style={{ color: colors.accent }}>$</span> pip install entroplain</div>
            <div style={{ marginTop: '20px' }}><span style={{ color: colors.accent }}>$</span> entroplain-proxy --port 8765 --provider openai</div>
            <div style={{ marginTop: '12px', color: colors.textMuted }}>→ Proxy running on http://localhost:8765</div>
            <div style={{ marginTop: '8px', color: colors.textMuted }}>→ Dashboard at http://localhost:8765/dashboard</div>
            <div style={{ marginTop: '20px' }}><span style={{ color: colors.accent }}>$</span> export OPENAI_BASE_URL=http://localhost:8765</div>
            <div style={{ marginTop: '20px', color: colors.accentLight }}>✓ Your agent now exits early when confident</div>
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section id="how" style={{
        position: 'relative',
        background: `linear-gradient(180deg, transparent, rgba(34, 197, 94, 0.02), transparent)`,
        padding: '180px 24px',
        zIndex: 1,
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <h2 style={{
            fontSize: '56px',
            fontWeight: 300,
            letterSpacing: '-0.04em',
            textAlign: 'center',
            marginBottom: '96px',
            color: colors.textPrimary,
          }}>How it works</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px' }}>
            {[
              { num: '01', title: 'Monitor entropy', desc: 'Track token-level entropy in real-time. Low entropy means high confidence — the model knows the answer.', color: colors.accent },
              { num: '02', title: 'Detect valleys', desc: 'When entropy drops into a sustained valley, the model has converged on a confident, stable answer.', color: '#3b82f6' },
              { num: '03', title: 'Exit early', desc: 'Stop generation once confidence is established. Save up to 50% tokens without quality loss.', color: '#a855f7' },
            ].map((step, i) => (
              <div key={i} style={{
                background: colors.darkSurface,
                borderRadius: '16px',
                padding: '48px 36px',
                border: `1px solid ${colors.borderSubtle}`,
                transition: 'all 0.3s',
              }}>
                <div style={{
                  fontSize: '13px',
                  fontWeight: 600,
                  color: step.color,
                  marginBottom: '20px',
                  fontFamily: 'monospace',
                  letterSpacing: '0.05em',
                }}>{step.num}</div>
                <h3 style={{
                  fontSize: '28px',
                  fontWeight: 500,
                  letterSpacing: '-0.02em',
                  marginBottom: '20px',
                  color: colors.textPrimary,
                }}>{step.title}</h3>
                <p style={{ color: colors.textSecondary, lineHeight: 1.7, margin: 0, fontSize: '16px' }}>{step.desc}</p>
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
        padding: '180px 24px',
        zIndex: 1,
      }}>
        <h2 style={{
          fontSize: '56px',
          fontWeight: 300,
          letterSpacing: '-0.04em',
          textAlign: 'center',
          marginBottom: '96px',
          color: colors.textPrimary,
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
              background: colors.darkSurface,
              borderRadius: '14px',
              padding: '36px',
              border: `1px solid ${colors.borderSubtle}`,
              transition: 'all 0.3s',
            }}>
              <h3 style={{
                fontSize: '20px',
                fontWeight: 600,
                letterSpacing: '-0.01em',
                marginBottom: '12px',
                color: colors.textPrimary,
              }}>{f.title}</h3>
              <p style={{ color: colors.textSecondary, lineHeight: 1.65, margin: 0, fontSize: '15px' }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Stats - Linear-style gradient section */}
      <section style={{
        position: 'relative',
        background: `linear-gradient(135deg, ${colors.darkSurface} 0%, #0f1015 100%)`,
        padding: '140px 24px',
        zIndex: 1,
        borderTop: `1px solid ${colors.borderSubtle}`,
        borderBottom: `1px solid ${colors.borderSubtle}`,
      }}>
        <div style={{
          maxWidth: '1100px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '80px',
          textAlign: 'center',
        }}>
          <div>
            <div style={{ fontSize: '96px', fontWeight: 300, letterSpacing: '-0.05em', color: colors.accentLight, marginBottom: '12px', whiteSpace: 'nowrap' }}>50%</div>
            <div style={{ color: colors.textSecondary, fontSize: '18px', letterSpacing: '0.02em' }}>Token savings</div>
          </div>
          <div>
            <div style={{ fontSize: '96px', fontWeight: 300, letterSpacing: '-0.05em', color: colors.textPrimary, marginBottom: '12px', whiteSpace: 'nowrap' }}>0</div>
            <div style={{ color: colors.textSecondary, fontSize: '18px', letterSpacing: '0.02em' }}>Code changes</div>
          </div>
          <div>
            <div style={{ fontSize: '96px', fontWeight: 300, letterSpacing: '-0.05em', color: colors.textPrimary, marginBottom: '12px', whiteSpace: 'nowrap' }}>6+</div>
            <div style={{ color: colors.textSecondary, fontSize: '18px', letterSpacing: '0.02em' }}>LLM providers</div>
          </div>
        </div>
      </section>

      {/* Supported Providers */}
      <section style={{
        position: 'relative',
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '140px 24px',
        textAlign: 'center',
        zIndex: 1,
      }}>
        <h3 style={{
          fontSize: '13px',
          fontWeight: 600,
          color: colors.textMuted,
          marginBottom: '40px',
          textTransform: 'uppercase',
          letterSpacing: '0.15em',
        }}>Works with any provider that exposes logprobs</h3>
        
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '16px',
        }}>
          {['OpenAI', 'Anthropic Claude', 'NVIDIA NIM', 'Google Gemini', 'OpenRouter', 'Ollama', 'Together AI', 'Groq'].map((p) => (
            <div key={p} style={{
              padding: '12px 24px',
              background: colors.darkSurface,
              borderRadius: '10px',
              border: `1px solid ${colors.borderSubtle}`,
              color: colors.textSecondary,
              fontSize: '15px',
              fontWeight: 500,
            }}>{p}</div>
          ))}
        </div>
      </section>

      {/* Final CTA - Linear-inspired gradient */}
      <section style={{
        position: 'relative',
        maxWidth: '960px',
        margin: '0 auto 140px',
        padding: '0 24px',
        zIndex: 1,
      }}>
        <div style={{
          background: `linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%)`,
          borderRadius: '28px',
          padding: '100px 72px',
          textAlign: 'center',
          border: `1px solid rgba(34, 197, 94, 0.15)`,
          position: 'relative',
          overflow: 'hidden',
        }}>
          {/* Subtle gradient overlay */}
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'radial-gradient(ellipse at center, rgba(34, 197, 94, 0.1), transparent 70%)',
            pointerEvents: 'none',
          }} />
          <h2 style={{
            position: 'relative',
            fontSize: '48px',
            fontWeight: 300,
            letterSpacing: '-0.03em',
            color: colors.textPrimary,
            marginBottom: '20px',
          }}>Start saving tokens today</h2>
          <p style={{
            position: 'relative',
            color: colors.textSecondary,
            marginBottom: '40px',
            fontSize: '20px',
          }}>
            Install in 30 seconds. No code changes. Works with your existing agent setup.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '20px', position: 'relative' }}>
            <a href="https://pypi.org/project/entroplain/" style={{
              padding: '18px 40px',
              background: colors.accent,
              color: 'white',
              borderRadius: '10px',
              textDecoration: 'none',
              fontSize: '17px',
              fontWeight: 600,
              boxShadow: `0 8px 24px rgba(34, 197, 94, 0.35)`,
            }}>pip install entroplain</a>
            <a href="https://github.com/entroplain/entroplain" style={{
              padding: '18px 40px',
              background: 'rgba(255, 255, 255, 0.05)',
              color: colors.textPrimary,
              borderRadius: '10px',
              textDecoration: 'none',
              fontSize: '17px',
              fontWeight: 500,
              border: `1px solid ${colors.borderSubtle}`,
            }}>View on GitHub</a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        position: 'relative',
        borderTop: `1px solid ${colors.borderSubtle}`,
        padding: '56px 24px',
        zIndex: 1,
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '28px',
              height: '28px',
              borderRadius: '6px',
              background: `linear-gradient(135deg, ${colors.accent}, ${colors.accentLight})`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <span style={{ color: 'white', fontWeight: 700, fontSize: '12px' }}>E</span>
            </div>
            <span style={{ fontWeight: 500, fontSize: '16px', letterSpacing: '-0.02em' }}>Entroplain</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '40px' }}>
            <a href="https://github.com/entroplain/entroplain" style={{ color: colors.textMuted, textDecoration: 'none', fontSize: '15px', transition: 'color 0.2s' }}>GitHub</a>
            <a href="https://pypi.org/project/entroplain/" style={{ color: colors.textMuted, textDecoration: 'none', fontSize: '15px', transition: 'color 0.2s' }}>PyPI</a>
            <a href="https://www.npmjs.com/package/entroplain" style={{ color: colors.textMuted, textDecoration: 'none', fontSize: '15px', transition: 'color 0.2s' }}>npm</a>
            <a href="https://github.com/entroplain/entroplain/blob/main/LICENSE" style={{ color: colors.textMuted, textDecoration: 'none', fontSize: '15px', transition: 'color 0.2s' }}>MIT License</a>
          </div>
        </div>
      </footer>
    </main>
  )
}
