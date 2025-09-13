import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='AceE6data SQL Analysis Tool')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--dashboard', action='store_true', help='Launch dashboard')
    
    args = parser.parse_args()
    
    if args.dashboard:
        from sql_dashboard import demo
        demo.launch()
    elif args.cli:
        # Import and run your CLI functionality
        from cli_module import run_cli
        run_cli()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()