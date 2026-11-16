import React, {useMemo} from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Word} from '../types';
import {body, clamp, display} from '../theme';

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9%$]/g, '');

/** Split the narration into short on-screen phrases of up to three words. */
const chunkWords = (words: Word[]): Word[][] => {
  const chunks: Word[][] = [];
  let cur: Word[] = [];
  let chars = 0;
  words.forEach((w, i) => {
    const prev = words[i - 1];
    const gap = prev ? w.startMs - prev.endMs : 0;
    const prevEndsPhrase = prev ? /[.,!?;:]$/.test(prev.text) : false;
    if (cur.length && (cur.length >= 3 || chars + w.text.length > 18 || gap > 280 || prevEndsPhrase)) {
      chunks.push(cur);
      cur = [];
      chars = 0;
    }
    cur.push(w);
    chars += w.text.length;
  });
  if (cur.length) chunks.push(cur);
  return chunks;
};

export const Captions: React.FC<{
  words: Word[];
  emphasis: string[];
  accent: string;
  style?: 'pop' | 'box' | 'pill';
}> = ({words, emphasis, accent, style = 'pop'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const chunks = useMemo(() => chunkWords(words), [words]);
  const emph = useMemo(() => new Set(emphasis.map(norm)), [emphasis]);

  if (!chunks.length) return null;
  let idx = chunks.findIndex((c) => ms < c[c.length - 1].endMs + 100);
  if (idx === -1) idx = chunks.length - 1;
  const chunk = chunks[idx];

  return (
    <div
      style={{
        position: 'absolute',
        top: 290,
        left: 70,
        right: 70,
        height: 200,
        display: 'flex',
        flexWrap: 'wrap',
        alignItems: 'center',
        alignContent: 'center',
        justifyContent: 'center',
        columnGap: 20,
        textShadow: '0 4px 30px rgba(0,0,0,0.8)',
      }}
    >
      {chunk.map((w, i) => {
        const strong = emph.has(norm(w.text));
        const t = interpolate(ms, [w.startMs - 40, w.startMs + 110], [0, 1], clamp);
        const look: React.CSSProperties = !strong
          ? {fontFamily: body, fontWeight: 600, fontSize: 66, color: '#fff'}
          : style === 'box'
            ? {
                fontFamily: body,
                fontWeight: 700,
                fontSize: 70,
                color: '#fff',
                padding: '0 16px',
                border: `3px solid ${accent}`,
                borderRadius: 8,
                background: `${accent}2e`,
              }
            : style === 'pill'
              ? {
                  fontFamily: body,
                  fontWeight: 700,
                  fontSize: 70,
                  color: '#0a0a0a',
                  padding: '0 22px',
                  borderRadius: 18,
                  background: accent,
                  textShadow: 'none',
                }
              : {fontFamily: display, fontWeight: 400, fontSize: 96, color: accent};
        return (
          <span
            key={`${idx}-${i}`}
            style={{
              ...look,
              lineHeight: 1.15,
              opacity: t,
              transform: `translateY(${(1 - t) * 18}px) scale(${0.92 + t * 0.08})`,
              display: 'inline-block',
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
