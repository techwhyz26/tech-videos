import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');

/** props: { lines: string[] (2-4 short lines), highlight?: string[] } - big kinetic typography that slams in. */
export const WordsScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines: string[] = (props.lines ?? []).slice(0, 4);
  const hi = new Set<string>((props.highlight ?? []).map(norm));
  const step = Math.min(9, Math.max(4, Math.floor((frames * 0.5) / Math.max(1, lines.length))));

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 540,
          left: 50,
          right: 50,
          height: 920,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          transform: 'rotate(-3deg)',
        }}
      >
        {lines.map((line, i) => {
          const t = pop(frame, fps, 3 + i * step, 11);
          const size = Math.max(110, Math.min(300, 900 / (Math.max(3, line.length) * 0.46)));
          const dir = i % 2 === 0 ? -1 : 1;
          return (
            <div
              key={i}
              style={{
                fontFamily: display,
                fontSize: size,
                lineHeight: 1.02,
                textTransform: 'uppercase',
                whiteSpace: 'nowrap',
                opacity: Math.min(1, t * 1.4),
                transform: `translateX(${(1 - t) * dir * 500}px) scale(${1.25 - t * 0.25})`,
              }}
            >
              {line.split(/\s+/).map((w, j) => {
                const strong = hi.has(norm(w));
                return (
                  <span
                    key={j}
                    style={{
                      color: strong ? accent : '#fff',
                      textShadow: strong ? `0 0 70px ${accent}aa` : 'none',
                      marginRight: size * 0.2,
                    }}
                  >
                    {w}
                  </span>
                );
              })}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
