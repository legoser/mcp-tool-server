#!/usr/bin/env python3
"""Debug script to inspect Tool object structure."""

if __name__ == "__main__":
    import sys
    sys.path.insert(0, '/home/ej/Code/PetProjects/MCP-tools-server')
    
    from src.server import create_server
    
    server = create_server()
    print(f"✓ Server created with {len(server.tools)} tools\n")
    
    if server.tools:
        tool = server.tools[2]  # get_random_quote
        print(f"Tool name: {tool.name}")
        print(f"Tool type: {type(tool).__name__}")
        print(f"Tool module: {type(tool).__module__}\n")
        
        print("=" * 60)
        print("PUBLIC ATTRIBUTES:")
        print("=" * 60)
        for attr in sorted(dir(tool)):
            if not attr.startswith('_'):
                try:
                    val = getattr(tool, attr)
                    if callable(val):
                        print(f"  ✓ {attr}: <callable>")
                    else:
                        print(f"    {attr}: {type(val).__name__}")
                except:
                    pass
        
        print("\n" + "=" * 60)
        print("LOOKING FOR FUNCTION:")
        print("=" * 60)
        
        # Check specific attributes
        for attr in ['function', 'fn', '_impl', 'impl', '_function', '_fn', 'handler', '_handler']:
            if hasattr(tool, attr):
                val = getattr(tool, attr)
                print(f"  ✓ Found: {attr}")
                print(f"    Type: {type(val)}")
                print(f"    Callable: {callable(val)}")
                if callable(val):
                    import inspect
                    sig = inspect.signature(val)
                    print(f"    Signature: {sig}")
                break
        
        # If Tool is a Pydantic model, check model_fields
        if hasattr(tool, 'model_fields'):
            print(f"\n  Model fields: {list(tool.model_fields.keys())}")
        
        print("\n✓ Debug complete")
