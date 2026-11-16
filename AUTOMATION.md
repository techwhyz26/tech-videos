# Running the pipeline in the cloud

Once this is set up, your PC can stay off:

```
every day 05:00 UTC   GitHub Actions: pick a topic -> Claude writes + draws -> voice -> render
                      -> the video arrives in Telegram with  [✅ Post it]  [❌ Reject]
every hour            GitHub Actions: reads your taps -> posts approved videos through Upload-Post
                      -> replies in Telegram with the links
```

Days alternate between a tech-news video and a how-it-works explainer. You can also make one on demand:
GitHub -> your repository -> **Actions** -> **Make a video** -> **Run workflow** (pick the kind, or type
your own idea). Taps are acted on within about an hour.

## What it costs

| Piece | Cost |
|---|---|
| GitHub Actions | Free. A private repository gets 2,000 minutes a month; this uses roughly 900-1,200 (one render of 10-20 minutes a day plus a one-minute check every hour). A public repository has no limit. |
| Telegram bot | Free |
| Voice (edge-tts) | Free |
| Claude API | Pay per use, billed by Anthropic. Each video is one long request (script + 12-18 drawings) plus two small ones. Check the usage page in the Claude Console after the first few videos, and set a monthly spend limit there. |
| Upload-Post | Free plan: 10 uploads a month, Instagram / YouTube / Facebook and others, **no TikTok**. Basic plan ($24 a month, $16 billed yearly): unlimited uploads and TikTok. |

## One-time setup (about 30 minutes)

You create the accounts and paste the keys yourself. Never send keys in a chat or put them in a file
in this folder; they go only into GitHub's encrypted **Secrets**.

### 1. Claude API key
1. Sign in at https://platform.claude.com and add a payment method under **Billing**.
2. Set a monthly spend limit under **Limits**, so a mistake can never cost more than you chose.
3. **API keys** -> **Create key**. Copy it (it starts with `sk-ant-`). This is `ANTHROPIC_API_KEY`.

### 2. Upload-Post and your social accounts
1. Instagram: switch to a **Professional** account (Settings -> Account type and tools -> Switch to
   professional account -> Creator or Business) and link it to a Facebook Page.
2. Sign up at https://www.upload-post.com and create a profile. Use the name `techwhyz`, or
   change `automation.upload_post_user` in `config.json` to the name you chose.
3. In that profile, connect Instagram, YouTube and Facebook (and TikTok if you upgrade).
4. Copy your API key from the Upload-Post dashboard. This is `UPLOAD_POST_API_KEY`.
5. `automation.platforms` in `config.json` lists where videos go. Add `"tiktok"` once your plan includes it.

### 3. Telegram bot
1. In Telegram, open **@BotFather**, send `/newbot`, and pick a name and a username ending in `bot`.
2. BotFather replies with a token like `123456:ABC...`. This is `TELEGRAM_BOT_TOKEN`.
3. Open your new bot and send it any message (for example `hi`).
4. On your PC, in this folder, run (paste your token between the quotes):
   ```
   $env:TELEGRAM_BOT_TOKEN = "paste-token-here"; python run.py telegram-setup
   ```
   It prints `TELEGRAM_CHAT_ID = ...`. Only taps from this chat are obeyed, so a stranger who finds
   your bot cannot post anything.

### 4. GitHub repository
1. Create a free account at https://github.com.
2. In this folder, sign in and create a **private** repository with the code:
   ```
   gh auth login
   gh repo create tech-videos --private --source . --push
   ```
3. Add the four secrets (each command asks you to paste the value):
   ```
   gh secret set ANTHROPIC_API_KEY
   gh secret set UPLOAD_POST_API_KEY
   gh secret set TELEGRAM_BOT_TOKEN
   gh secret set TELEGRAM_CHAT_ID
   ```
   (Or on github.com: repository -> Settings -> Secrets and variables -> Actions -> New repository secret.)

### 5. First test
1. GitHub -> repository -> **Actions** -> **Make a video** -> **Run workflow**.
2. After 15-25 minutes the video arrives in Telegram. Watch it before you tap.
3. Tap ✅, then either wait for the hourly check or run **Post approved videos** by hand.

## Day to day

- **Change the time**: edit the `cron` line in `.github/workflows/make-video.yml` (times are UTC).
- **More than one video a day**: add a second `cron` line.
- **A video failed**: Telegram gets a message with a link to the log.
- **A drawing came out wrong**: tap ❌. To fix it instead, pull the repository on your PC, edit
  `public/videos/<slug>/art/scene-NN.svg` (or ask Claude Code to), run `python run.py build <slug>`,
  then `python run.py send-review <slug>` with your Telegram variables set.
- **Pause everything**: Actions -> each workflow -> **...** -> **Disable workflow**.

## Things to know

- The quality bar is the `qr-code-damage` and `microwave-wifi` videos. Claude is asked to match them and
  scripts with template scenes are rejected, but drawings made unattended will vary. That is why
  nothing is posted until you tap ✅.
- The free voice service sometimes refuses connections from cloud servers. If the voice step keeps
  failing, the fallback is a paid voice API.
- GitHub pauses scheduled workflows in repositories with no activity for 60 days. The daily commits
  count as activity, so this only matters if the workflow keeps failing.
- Each video is stored as a GitHub release named `video-<slug>` (in a private repository only you can
  see it). Delete old ones under Releases when you no longer need them.
