import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';
import {Icon} from '../components/Icon';

/** props: { time?: string, icon?: string, title?: string, lines?: string[] (up to 4) } - a phone screen with rows sliding in. */
export const PhoneScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines: string[] = (props.lines ?? []).slice(0, 4);
  const t = pop(frame, fps, 2, 12);
  const step = Math.min(10, Math.max(4, Math.floor((frames * 0.45) / Math.max(1, lines.length))));
  const W = 580;
  const H = 960;
  const L = (1080 - W) / 2;
  const T = 540;
  const tilt = Math.sin(frame / 40) * 1.5;

  return (
    <AbsoluteFill>
      {[0, 1].map((i) => {
        const p = ((frame + i * 25) % 50) / 50;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: L - 30,
              top: T - 30,
              width: W + 60,
              height: H + 60,
              borderRadius: 120,
              border: `3px solid ${accent}`,
              opacity: (1 - p) * 0.45 * t,
              transform: `scale(${1 + p * 0.22})`,
            }}
          />
        );
      })}
      <div
        style={{
          position: 'absolute',
          left: L,
          top: T,
          width: W,
          height: H,
          borderRadius: 96,
          border: '8px solid rgba(255,255,255,0.3)',
          background: `linear-gradient(170deg, #0b0b10 30%, ${accent}55 130%)`,
          boxShadow: `0 60px 140px rgba(0,0,0,0.7), 0 0 100px ${accent}44`,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: '34px 34px 44px',
          opacity: t,
          transform: `translateY(${(1 - t) * 160}px) rotate(${tilt}deg)`,
        }}
      >
        <div style={{width: 170, height: 44, borderRadius: 22, background: '#000', border: '2px solid rgba(255,255,255,0.12)'}} />
        {props.time ? (
          <div style={{fontFamily: display, fontSize: 150, lineHeight: 1, marginTop: 50}}>{props.time}</div>
        ) : (
          <div style={{marginTop: 46}}>
            <Icon name={props.icon ?? 'phone'} size={150} color={accent} stroke={1.5} />
          </div>
        )}
        {props.title ? (
          <div style={{fontSize: 40, fontWeight: 700, marginTop: 22, textAlign: 'center'}}>{props.title}</div>
        ) : null}
        <div style={{flex: 1}} />
        <div style={{width: '100%', display: 'flex', flexDirection: 'column', gap: 18}}>
          {lines.map((line, i) => {
            const k = pop(frame, fps, 12 + i * step);
            return (
              <div
                key={i}
                style={{
                  padding: '24px 28px',
                  borderRadius: 30,
                  background: 'rgba(255,255,255,0.14)',
                  border: '2px solid rgba(255,255,255,0.12)',
                  fontSize: 34,
                  fontWeight: 600,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 18,
                  opacity: k,
                  transform: `translateY(${(1 - k) * 70}px)`,
                }}
              >
                <span style={{width: 18, height: 18, borderRadius: '50%', background: accent, flexShrink: 0}} />
                {line}
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
