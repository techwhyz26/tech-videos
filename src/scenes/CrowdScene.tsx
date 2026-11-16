import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {BG, display, pop} from '../theme';

const ROWS = [
  {y: 1010, n: 4, size: 130, shift: 0},
  {y: 1150, n: 5, size: 160, shift: 0.5},
  {y: 1330, n: 4, size: 200, shift: 0},
  {y: 1560, n: 5, size: 250, shift: 0.5},
];

const glass = (a: number) =>
  `radial-gradient(circle at 35% 28%, rgba(255,255,255,${a}), rgba(255,255,255,${a * 0.12}) 62%, rgba(255,255,255,${a * 0.3}) 100%)`;

/** props: { symbol?: string } - an audience of glass figures reacting to a big symbol. */
export const CrowdScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const symbol: string = props.symbol ?? '!';
  const s = pop(frame, fps, 14, 9);
  const shake = Math.sin(frame / 2.2) * Math.max(0, 1 - (frame - 14) / 24) * 6;

  return (
    <AbsoluteFill>
      {/* spotlight */}
      <div
        style={{
          position: 'absolute',
          top: -200,
          left: -150,
          width: 700,
          height: 1500,
          transform: 'rotate(-32deg)',
          transformOrigin: 'top left',
          background: 'linear-gradient(180deg, rgba(255,255,255,0.16), transparent 75%)',
          filter: 'blur(40px)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: 520,
          left: 0,
          right: 0,
          textAlign: 'center',
          fontFamily: display,
          fontSize: 400,
          lineHeight: 1,
          color: '#fff',
          textShadow: `0 0 80px ${accent}`,
          opacity: Math.min(1, s * 1.5),
          transform: `translateX(${shake}px) scale(${0.3 + s * 0.7})`,
        }}
      >
        {symbol}
      </div>
      {ROWS.map((row, r) =>
        Array.from({length: row.n + 1}).map((_, i) => {
          const spacing = 1080 / row.n;
          const x = (i + row.shift) * spacing - (row.shift ? spacing / 2 : 0) + spacing / 2;
          const t = pop(frame, fps, r * 3 + i * 2);
          const bob = Math.sin(frame / 14 + i * 1.7 + r) * 6;
          const a = 0.16 + r * 0.05;
          return (
            <div
              key={`${r}-${i}`}
              style={{
                position: 'absolute',
                left: x - row.size * 1.1,
                top: row.y + bob,
                width: row.size * 2.2,
                opacity: t,
                transform: `translateY(${(1 - t) * 260}px)`,
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  left: row.size * 0.6,
                  top: 0,
                  width: row.size,
                  height: row.size,
                  borderRadius: '50%',
                  background: glass(a + 0.12),
                  border: '2px solid rgba(255,255,255,0.28)',
                  boxShadow: '0 0 40px rgba(0,0,0,0.6)',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  left: 0,
                  top: row.size * 0.82,
                  width: row.size * 2.2,
                  height: row.size * 2.2,
                  borderRadius: '50%',
                  background: glass(a),
                  border: '2px solid rgba(255,255,255,0.14)',
                }}
              />
            </div>
          );
        }),
      )}
      {/* fade crowd into the bottom safe area */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          bottom: 0,
          height: 520,
          background: `linear-gradient(180deg, transparent, ${BG} 85%)`,
        }}
      />
    </AbsoluteFill>
  );
};
