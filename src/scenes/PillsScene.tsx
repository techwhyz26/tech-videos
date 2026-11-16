import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {clamp, display, pop} from '../theme';

const DOTS = ['#ff5a5f', '#ffb020', '#3b82f6', '#22c55e', '#a855f7', '#06b6d4', '#f43f5e'];

/** props: { items: string[], result?: { value: string, label?: string } } - a list bracketed into one result. */
export const PillsScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items: string[] = (props.items ?? []).slice(0, 7);
  const result = props.result as {value: string; label?: string} | undefined;
  const H = 100;
  const GAP = 30;
  const total = items.length * H + (items.length - 1) * GAP;
  const mid = 990;
  const top = mid - total / 2;
  const bot = top + total;
  const step = Math.min(6, Math.max(3, Math.floor((frames * 0.4) / Math.max(1, items.length))));
  const afterList = 6 + items.length * step;
  const brace = interpolate(frame, [afterList, afterList + 16], [0, 1], clamp);
  const res = pop(frame, fps, afterList + 12);
  const value = result?.value ?? '';

  return (
    <AbsoluteFill>
      {items.map((label, i) => {
        const t = pop(frame, fps, 4 + i * step);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 90,
              top: top + i * (H + GAP),
              height: H,
              maxWidth: 440,
              padding: '0 40px 0 30px',
              display: 'flex',
              alignItems: 'center',
              gap: 20,
              borderRadius: H / 2,
              background: '#fff',
              color: '#111',
              fontSize: 42,
              fontWeight: 600,
              whiteSpace: 'nowrap',
              boxShadow: '0 10px 40px rgba(0,0,0,0.5)',
              opacity: t,
              transform: `translateX(${(1 - t) * -90}px)`,
            }}
          >
            <span
              style={{
                width: 26,
                height: 26,
                borderRadius: '50%',
                background: DOTS[i % DOTS.length],
                flexShrink: 0,
              }}
            />
            <span style={{overflow: 'hidden', textOverflow: 'ellipsis'}}>{label}</span>
          </div>
        );
      })}

      {result ? (
        <>
          <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
            <path
              d={`M 570 ${top} Q 625 ${top} 625 ${top + 50} L 625 ${mid - 50} Q 625 ${mid} 670 ${mid} Q 625 ${mid} 625 ${mid + 50} L 625 ${bot - 50} Q 625 ${bot} 570 ${bot}`}
              fill="none"
              stroke={accent}
              strokeWidth={6}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - brace}
            />
          </svg>
          <div
            style={{
              position: 'absolute',
              left: 690,
              top: mid - 160,
              width: 320,
              height: 320,
              borderRadius: '50%',
              border: '14px solid rgba(255,255,255,0.14)',
              boxShadow: `0 0 90px ${accent}66, inset 0 0 60px ${accent}33`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: display,
              fontSize: value.length > 4 ? 84 : 120,
              opacity: res,
              transform: `scale(${0.6 + res * 0.4})`,
            }}
          >
            {value}
          </div>
          {result.label ? (
            <div
              style={{
                position: 'absolute',
                left: 650,
                width: 400,
                top: mid + 190,
                textAlign: 'center',
                fontSize: 38,
                fontWeight: 600,
                lineHeight: 1.25,
                color: 'rgba(255,255,255,0.8)',
                opacity: res,
              }}
            >
              {result.label}
            </div>
          ) : null}
        </>
      ) : null}
    </AbsoluteFill>
  );
};
