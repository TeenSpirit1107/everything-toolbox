import os
import subprocess
import time

script_ls = ["test1.sh", "test2.sh", "test3.sh"]
time_interval = 5  # minutes
base_dir = "/home/ubuntu/test_script"

def main():
    """Run scripts from the list in a loop; wait the configured interval after each run."""
    # Change to the base directory
    os.chdir(base_dir)

    script_index = 0

    while True:
        # Script to run this iteration
        script = script_ls[script_index]
        script_path = os.path.join(base_dir, script)

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running script: {script}")

        try:
            # Execute the script
            result = subprocess.run(
                ["bash", script_path],
                cwd=base_dir,
                check=False,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"Script {script} finished successfully")
            else:
                print(f"Script {script} failed with exit code: {result.returncode}")
                if result.stderr:
                    print(f"Stderr: {result.stderr}")
        except Exception as e:
            print(f"Exception while running script {script}: {e}")

        # Next script (wrap around)
        script_index = (script_index + 1) % len(script_ls)

        # Wait for the configured interval
        print(f"Waiting {time_interval} minute(s) before the next script...")
        time.sleep(time_interval * 60)

if __name__ == "__main__":
    main()
