import subprocess

def run_shell_script_as_sudo():
    # Path to the shell script
    script_path = '/home/arducam/bin/foobaroo.sh'

    try:
        # Run the shell script with sudo
        result = subprocess.run(['sudo', script_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Output the result
        print("Script output:")
        print(result.stdout)
    
    except subprocess.CalledProcessError as e:
        print(f"Error running the script as sudo: {e}")
        print(f"Script error output: {e.stderr}")

if __name__ == "__main__":
    run_shell_script_as_sudo()

