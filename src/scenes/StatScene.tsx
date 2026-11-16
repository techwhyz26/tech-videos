import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';

/** props: { value: number, prefix?: string, suffix?: string, decimals?: number, label?: string, ring?: number (0-1) } */
export const StatScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const value: number = Number(props.value ?? 0);
  const decimals: number = props.decimals ?? 0;
  const ringTo: number = props.ring ?? 1;
  const dur = Math.min(45, Math.max(15, Math.floor(frames * 0.5)));
  const t = interpolate(frame, [6, 6 + dur], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const text = `${props.prefix ?? ''}${(value * t).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })}${props.suffix ?? ''}`;
  const R = 310;
  const C = 2 * Math.PI * R;
  const label = pop(frame, fps, 6 + dur - 6);
  const inn = pop(frame, fps, 0);

  return (
    <AbsoluteFill>
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, opacity: inn}}>
        <circle cx={540} cy={960} r={R} fill="none" stroke="rgba(255,255,255,0.09)" strokeWidth={26} />
        <circle
          cx={540}
          cy={960}
          r={R}
          fill="none"
          stroke={accent}
          strokeWidth={26}
          strokeLinecap="round"
          strokeDasharray={C}
          strokeDashoffset={C * (1 - ringTo * t)}
          transform="rotate(-90 540 960)"
          style={{filter: `drop-shadow(0 0 24px ${accent})`}}
        />
      </svg>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 960 - 130,
          height: 260,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: display,
          fontSize: text.length > 6 ? 130 : text.length > 4 ? 170 : 220,
          opacity: inn,
        }}
      >
        {text}
      </div>
      {props.label ? (
        <div
          style={{
            position: 'absolute',
            left: 120,
            right: 120,
            top: 1350,
            textAlign: 'center',
            fontSize: 52,
            fontWeight: 600,
            lineHeight: 1.25,
            opacity: label,
            transform: `translateY(${(1 - label) * 30}px)`,
          }}
        >
          {props.label}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
