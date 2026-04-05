examples:
  - |
    # Python
    from entroplain import EntropyMonitor
    
    monitor = EntropyMonitor()
    monitor.track("Hello", 0.5)
    
    if monitor.should_exit():
        print("Reasoning complete!")
    
  - |
    # CLI
    entroplain analyze "What is 2+2?" --model gpt-4o
  
  - |
    # With OpenAI
    from entroplain import NVIDIAProvider, EntropyMonitor
    
    provider = NVIDIAProvider()
    monitor = EntropyMonitor()
    
    for token in provider.stream_with_entropy(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "user", "content": "Hello"}]
    ):
        monitor.track(token.token, token.entropy)
        if monitor.should_exit():
            break
  
  - |
    # Agent hook
    from entroplain.hooks import EntropyHook
    
    hook = EntropyHook(config={"entropy_threshold": 0.15})
    
    for token in agent.generate():
        result = hook.on_token(token, entropy)
        if result["should_exit"]:
            break
