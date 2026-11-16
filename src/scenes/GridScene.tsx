import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {clamp, display, pop} from '../theme';

const COLS = 20;
const CELL = 45;

/** props: { count?: number (max 300), fraction?: 0-1, value?: string, label?: string } - a field of dots lighting up. */
export const GridScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const count = Math.min(300, Math.max(COLS, Math.round(props.count ?? 300)));
  const fraction: number = props.fraction ?? 1;
  const rows = Math.ceil(count / COLS);
  const dur = Math.min(50, Math.max(15, Math.floor(frames * 0.55)));
  const lit = interpolate(frame, [6, 6 + dur], [0, count * fraction], clamp);
  const top = 600 + (15 - rows) * CELL * 0.5;
  const txt = pop(frame, fps, 6 + dur - 10);

  return (
    <AbsoluteFill>
      {Array.from({length: count}).map((_, i) => {
        // light the dots in a scattered order when only part of the grid lights up, as a sweep otherwise
        const order = fraction < 1 ? (i * 7919) % count : i;
        const on = order < lit;
        const row = Math.floor(i / COLS);
        const col = i % COLS;
        const wave = Math.sin(frame / 6 - (row + col) / 3) * 0.15;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 90 + col * CELL + 11,
              top: top + row * CELL + 11,
              width: 22,
              height: 22,
              borderRadius: '50%',
              background: on ? accent : 'rgba(255,255,255,0.13)',
              boxShadow: on ? `0 0 18px ${accent}` : 'none',
              transform: `scale(${on ? 1.1 + wave : 0.8})`,
            }}
          />
        );
      })}
      {props.value ? (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: 1320,
            textAlign: 'center',
            fontFamily: display,
            fontSize: 150,
            lineHeight: 1,
            color: accent,
            opacity: txt,
            transform: `scale(${0.7 + txt * 0.3})`,
          }}
        >
          {props.value}
        </div>
      ) : null}
      {props.label ? (
        <div
          style={{
            position: 'absolute',
            left: 100,
            right: 100,
            top: props.value ? 1490 : 1340,
            textAlign: 'center',
            fontSize: 48,
            fontWeight: 600,
            opacity: txt,
          }}
        >
          {props.label}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
