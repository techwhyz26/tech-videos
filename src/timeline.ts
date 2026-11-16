import type {Scene, Spec, Word} from './types';

export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

export type TimedScene = Scene & {words: Word[]; from: number; frames: number};

/** Rough word timings, used only for previews before the voice step has run. */
const estimateWords = (narration: string): Word[] => {
  let t = 150;
  return narration
    .split(/\s+/)
    .filter(Boolean)
    .map((text) => {
      const len = 220 + text.length * 28;
      const w = {text, startMs: t, endMs: t + len};
      t += len + 30;
      return w;
    });
};

export const resolveTimeline = (spec: Spec): TimedScene[] => {
  let cursorMs = 0;
  return spec.scenes.map((s) => {
    const words = s.words && s.words.length ? s.words : estimateWords(s.narration);
    const lastEnd = words.length ? words[words.length - 1].endMs : 1500;
    const durationMs = s.durationMs ?? lastEnd + 400;
    const from = Math.round((cursorMs / 1000) * FPS);
    cursorMs += durationMs;
    const end = Math.round((cursorMs / 1000) * FPS);
    return {...s, words, from, frames: Math.max(1, end - from)};
  });
};

export const totalFrames = (spec: Spec): number => {
  const t = resolveTimeline(spec);
  const last = t[t.length - 1];
  return last ? last.from + last.frames : FPS;
};
