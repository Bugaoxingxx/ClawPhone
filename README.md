# ClawPhone
I recently started running OpenClaw on a $25 Android smartphone to have an isolated sandbox to try out OpenClaw and also figure out interesting use cases of having OpenClaw agents have full control of the hardware of the smartphone.

There were  a few tweaks I had to make, but eventually got it working reliably and now it just runs in the background inside termux on a tmux session and I can interact with it over Discord and use it like a normal OpenClaw agent and also do phone hardware tasks if needed. It's a cool formfactor for it to run on, very cheap way to get started with OpenClaw, and it's isolated and mobile, you can easily bring it with you anywhere.

You can get the moto g 2025 perepaid smartphone in the US for $30 on [Walmart.com](https://www.walmart.com/ip/Straight-Talk-Motorola-Moto-g-2025-5G-64GB-Blue-Prepaid-Smartphone-Locked-to-Straight-Talk/14552506783) or use any old Android 8+ phone you have lying around.

Here are some things to note if you try this:


0. Make sure you have the termux app installed. I would install `tmux`, a text editor like `nvim`, `nodejs-lts`, `python`. Also install the Termux:API and Termux:GUI apps and give everything full permissions so that OpenClaw will have full access to all the hardware if you want to use it for phone hardware tasks.
1. Install using the `npm install -g openclaw@latest` option and not the bash script they have as it will fail on Android.
2. During the installation it may fail the first few times on some dependencies, install those separately using `pkg` on termux and then start the installation again.
3. `llama.cpp` ships with it and because termux lacks glibc it will have to compile this from scratch which takes 15-30 minutes, just let it run.
4. When it first runs after installation it might have some errors saying there is no systemd which is accurate, don't panic. You can run the OpenClaw Gateway in the foreground (and maybe in a termux service not sure this is a TODO for me).
5. When you run `openclaw gateway` for the first time it will have errors saying it cannot access `/tmp/openclaw`. OpenClaw REALLY wants to create a directory in `/tmp` and use it for everything, but because we are on raw termux we do not have access to messaging with the `/tmp` directory of Android so we will get a lot of failures like that. The trick is to put this at the end of your `.bashrc` : 
```
export TMPDIR="$PREFIX/tmp"
export TMP="$TMPDIR"
export TEMP="$TMPDIR"
```
  6. You also want to make sure to add this to your `openclaw.json`:
  ```
   "logging": {
     "level": "info",
     "file": "/data/data/com.termux/files/usr/tmp/openclaw/openclaw-YYYY-MM-DD.log"
   }
  ```
  7. Also make sure a temp directory inside the termux route exists so run: `  mkdir -p /data/data/com.termux/files/usr/tmp/openclaw`
  8. After that do a `source .bashrc` and run `openclaw gateway` again and it should work.
  9. Next, you can do `openclaw onboard` and add your model token for whichever model you choose. I recommend using `tmux` and running the gateway in a tmux session as a way to keep track of it and keep it alive.
  10. Set the `gateway.bind` property to `lan` so that the Gateway can run as 0.0.0.0 that way you can hit the Dashboard from the phone's IP address on your local WiFi network.
  11. You probably want to tell OpenClaw it is living inside a termux app on a Android smartphone and that Termux:API and Termux:GUI are installed so it can utilize those things if it needs to for a particular task.




* You can also give OpenClaw the ability to write arbitrary things overlayed on top of the screen. Install Termux:GUI app and `pkg install termux-gui` inside termux and then run the `overlay_daemon.py` in a new window of the `tmux` session you have open and then instruct OpenClaw that it can use that daemon to write stuff to the screen for the user to see when needed.