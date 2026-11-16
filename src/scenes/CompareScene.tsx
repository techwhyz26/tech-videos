import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';

type Side = {label: string; value: number; display?: string};

/** props: { left: Side, right: Side } where Side = { label, value, display? } - two bars, the bigger one highlighted. */
export const CompareScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sides: Side[] = [props.left, props.right].filter(Boolean);
  const max = Math.max(1, ...sides.map((s) => Number(s.value) || 0));
  const BASE = 1420;
  const MAXH = 640;
  const W = 250;
  const xs = [330, 750];

  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 120, right: 120, top: BASE, height: 4, background: 'rgba(255,255,255,0.25)'}} />
      {sides.map((s, i) => {
        const big = Number(s.value) === max;
        const grow = interpolate(frame, [6 + i * 8, 34 + i * 8], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.out(Easing.cubic),
        });
        const h = Math.max(24, (Number(s.value) / max) * MAXH) * grow;
        const t = pop(frame, fps, 28 + i * 8);
        return (
          <React.Fragment key={i}>
            <div
              style={{
                position: 'absolute',
                left: xs[i] - W / 2,
                top: BASE - h,
                width: W,
                height: h,
                borderRadius: '28px 28px 0 0',
                background: big ? `linear-gradient(180deg, ${accent}, ${accent}77)` : 'rgba(255,255,255,0.22)',
                boxShadow: big ? `0 0 90px ${accent}88` : 'none',
              }}
            />
            <div
              style={{
                position: 'absolute',
                left: xs[i] - 220,
                width: 440,
                top: BASE - h - 140,
                textAlign: 'center',
                fontFamily: display,
                fontSize: 100,
                color: big ? accent : '#fff',
                opacity: t,
              }}
            >
              {s.display ?? String(s.value)}
            </div>
            <div
              style={{
                position: 'absolute',
                left: xs[i] - 220,
                width: 440,
                top: BASE + 34,
                textAlign: 'center',
                fontSize: 42,
                fontWeight: 600,
                lineHeight: 1.2,
              }}
            >
              {s.label}
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};
