# Video Automation Pipeline

Makes short vertical explainer videos (1080x1920, motion graphics + AI voice + word-by-word captions)
about how things work and technology news.

```
find topics  ->  write script  ->  voiceover  ->  render  ->  you approve  ->  publish
 RSS feeds       Claude            edge-tts       Remotion     run.py approve    (not connected yet)
```

## Commands

| Command | What it does |
|---|---|
| `python run.py topics` | Lists fresh tech stories from the feeds in `config.json` |
| `python run.py make --topic 3` | Script + voice + render for story number 3 |
| `python run.py make --idea "How does Wi-Fi work?"` | Same, from your own idea |
| `python run.py make --topic 3 --kind explainer` | `--kind news` (default for `--topic`) makes a tech-update video, `--kind explainer` a how-it-works video |
| `python run.py build <slug>` | Re-voice and re-render after you edit a spec by hand |
| `python run.py demo` | Builds the bundled sample (`samples/fast-charging.json`) |
| `python run.py status` | Lists every video and its stage |
| `python run.py voices` | Writes the same lines in six voices to `output/voice-samples/` so you can pick by ear |
| `python run.py approve <slug>` | Marks a rendered video as OK to post |
| `python run.py publish <slug>` | Posts an approved video (currently copies it to `output/ready/`) |
| `npm run studio` | Opens the Remotion editor to preview and tweak scenes live |

Finished videos land in `output/<slug>.mp4` with the caption in `output/<slug>.txt`.

## Script writing

`make` calls the Claude API, so it needs an API key from https://platform.claude.com in the
`ANTHROPIC_API_KEY` environment variable. Without a key you can still make videos: write or have
Claude Code write `public/videos/<slug>/spec.json` (copy the sample), then run `python run.py build <slug>`.

## The spec

Each video is one JSON file: a list of scenes, each with the sentence the voice says (`narration`),
the words to highlight in captions (`emphasis`), a scene `type` and its `props`.

| Type | Shows | Props |
|---|---|---|
| `title` | Big headline | `kicker`, `headline`, `highlight[]`, `sub` |
| `crowd` | Audience reacting to a symbol | `symbol` (`!` or `?`) |
| `pills` | A list bracketed into one result | `items[]`, `result {value, label}` |
| `hub` | Many things depending on one | `items[]`, `hub {label, icon}` |
| `steps` | One stage of a process | `steps[]`, `active`, `icon`, `status`, `progress` |
| `stat` | One big number in a ring | `value`, `prefix`, `suffix`, `decimals`, `ring`, `label` |
| `compare` | Two bars side by side | `left {label, value, display}`, `right {...}` |
| `icon` | One concept with a glowing icon | `icon`, `label`, `tags[]` |
| `words` | Huge kinetic text that slams in | `lines[]`, `highlight[]` |
| `chart` | A trend line that draws itself | `points[]`, `label`, `startLabel`, `endLabel`, `down` |
| `phone` | A phone screen with rows sliding in | `time`, `icon`, `title`, `lines[]` |
| `card` | News or announcement card | `source`, `date`, `headline`, `body` |
| `grid` | Field of dots lighting up | `count`, `fraction`, `value`, `label` |
| `image` | A photo with a slow zoom | `src` (file under `public/` or URL), `label`, `credit` |

| `art` | **A custom animated drawing of the actual subject** | `art` (name of a file in the video's `art/` folder) or `svg` |

### The standard: `qr-code-damage` and `microwave-wifi`

These two videos are the approved look. In both, every scene except the closing "Follow" card is an
`art` drawing of the real thing being talked about. `pipeline/script.py` requires the same of every
generated script: it rejects a script with other scene types and asks again (up to three tries). It also
shows Claude one approved drawing (`pipeline/example_art.svg`) as the bar to match. Generated drawings
are saved as `art/scene-NN.svg` so you can fix one by hand and run `build` again.

### Custom illustrations (`art`)

This is what stops videos looking like the same template. Each `art` scene is its own drawing: a real
QR code being torn, a microwave and a router sending out waves. A drawing is the inner markup of a
1000x1000 SVG animated with SMIL (`<animate>`, `<animateTransform>`), saved as
`public/videos/<slug>/art/<name>.svg` and referenced with `"props": {"art": "<name>"}`. Open the
`.svg` contents inside an `<svg viewBox="0 0 1000 1000">` in a browser to preview one.

`tools/art_qr.py` and `tools/art_microwave.py` show how the drawings for two videos were generated,
using the helpers in `tools/artlib.py` (expanding waves, pop-in badges, scrolling sine waves). When
scripts are written through the Claude API, the model is asked to draw the illustrations itself.

Any scene can take `"invert": true` to appear on a light background as a contrast beat.

## Themes

Six looks, each with its own colours, fonts, caption style and animated backdrop: `violet`, `ember`,
`matrix`, `ocean`, `gold`, `crimson` (defined in `src/theme.ts`). Set `"theme"` in the spec, or leave
it out and one is picked from the video's slug so consecutive videos differ.

## Script format

Scripts follow hook -> question -> one-line answer -> story with a mid-video re-hook -> payoff that
restates the hook -> call to action, at 150-210 words over 12-18 scenes. The rules live in the
`SYSTEM` prompt in `pipeline/script.py`.

Icon names are listed in `src/components/Icon.tsx`. New scene types go in `src/scenes/` and are
registered in `src/Video.tsx`.

## Settings

`config.json` holds the brand name and accent colour, the voice (`python -m edge_tts --list-voices`
shows the choices), the channel niche used when writing scripts, and the RSS feeds.

## Publishing

Posting goes through Upload-Post (`pipeline/publish.py`) once `UPLOAD_POST_API_KEY` is set; without
it, `publish` copies the video to `output/ready/`. To run everything daily in the cloud with Telegram
approval, follow [AUTOMATION.md](AUTOMATION.md).
