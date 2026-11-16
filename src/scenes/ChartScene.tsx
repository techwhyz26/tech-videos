import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {body, pop} from '../theme';

/** props: { points: number[], label?: string, startLabel?: string, endLabel?: string, down?: boolean } - a line that draws itself. */
export const ChartScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const points: number[] = (props.points ?? [1, 2]).map(Number);
  const color = props.down ? '#ff4d4d' : accent;
  const X0 = 140;
  const X1 = 900;
  const Y0 = 1330;
  const Y1 = 740;
  const min = Math.min(...points);
  const max = Math.max(...points);
  const px = (i: number) => X0 + ((X1 - X0) * i) / Math.max(1, points.length - 1);
  const py = (v: number) => Y0 - ((v - min) / Math.max(1e-9, max - min)) * (Y0 - Y1);

  const dur = Math.min(60, Math.max(20, Math.floor(frames * 0.6)));
  const p =
    interpolate(frame, [6, 6 + dur], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.inOut(Easing.cubic),
    }) *
    (points.length - 1);
  const whole = Math.floor(p);
  const frac = p - whole;
  const drawn = points.slice(0, whole + 1).map((v, i) => [px(i), py(v)]);
  let mx = px(whole);
  let my = py(points[whole]);
  if (whole < points.length - 1) {
    mx = px(whole) + (px(whole + 1) - px(whole)) * frac;
    my = py(points[whole]) + (py(points[whole + 1]) - py(points[whole])) * frac;
    drawn.push([mx, my]);
  }
  const line = drawn.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
  const area = `${line} L ${mx} ${Y0} L ${X0} ${Y0} Z`;
  const end = pop(frame, fps, 6 + dur - 4);
  const start = pop(frame, fps, 4);
  const tag: React.CSSProperties = {
    position: 'absolute',
    padding: '10px 26px',
    borderRadius: 18,
    fontFamily: body,
    fontSize: 44,
    fontWeight: 700,
    whiteSpace: 'nowrap',
  };

  return (
    <AbsoluteFill>
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        <defs>
          <linearGradient id="chart-fill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor={color} stopOpacity={0.45} />
            <stop offset="1" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        {[0, 1, 2, 3].map((i) => (
          <line
            key={i}
            x1={X0}
            x2={X1}
            y1={Y0 - ((Y0 - Y1) * i) / 3}
            y2={Y0 - ((Y0 - Y1) * i) / 3}
            stroke="rgba(255,255,255,0.1)"
            strokeWidth={2}
          />
        ))}
        <path d={area} fill="url(#chart-fill)" />
        <path d={line} fill="none" stroke={color} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
        <circle cx={mx} cy={my} r={30} fill={color} opacity={0.25} />
        <circle cx={mx} cy={my} r={15} fill="#fff" stroke={color} strokeWidth={6} />
      </svg>
      {props.startLabel ? (
        <div
          style={{
            ...tag,
            left: X0 - 10,
            top: py(points[0]) + 30,
            background: 'rgba(255,255,255,0.12)',
            opacity: start,
          }}
        >
          {props.startLabel}
        </div>
      ) : null}
      {props.endLabel ? (
        <div
          style={{
            ...tag,
            right: 1080 - X1 - 60,
            top: py(points[points.length - 1]) - 110,
            background: color,
            color: '#0a0a0a',
            opacity: end,
            transform: `scale(${0.6 + end * 0.4})`,
          }}
        >
          {props.endLabel}
        </div>
      ) : null}
      {props.label ? (
        <div
          style={{
            position: 'absolute',
            left: 100,
            right: 100,
            top: 1400,
            textAlign: 'center',
            fontSize: 50,
            fontWeight: 600,
            opacity: start,
          }}
        >
          {props.label}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
