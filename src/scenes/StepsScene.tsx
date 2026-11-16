import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {AMBER, BG, clamp, pop} from '../theme';
import {Icon} from '../components/Icon';

/** props: { steps: string[], active: number, icon?: string, status?: string, progress?: number } - one stage of a process. */
export const StepsScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const steps: string[] = (props.steps ?? []).slice(0, 5);
  const active: number = Math.min(steps.length - 1, Math.max(0, props.active ?? 0));
  const progress: number = props.progress ?? 1;
  const X0 = 150;
  const X1 = 930;
  const Y = 610;
  const xAt = (i: number) => (steps.length === 1 ? 540 : X0 + ((X1 - X0) * i) / (steps.length - 1));
  const line = interpolate(frame, [4, 24], [xAt(Math.max(0, active - 1)), xAt(active)], clamp);
  const card = pop(frame, fps, 6);
  const bar = interpolate(frame, [16, 46], [0, progress], clamp);
  const status = pop(frame, fps, 30);
  const ring = (frame % 40) / 40;

  return (
    <AbsoluteFill>
      {/* stepper */}
      <div style={{position: 'absolute', left: X0, top: Y - 3, width: X1 - X0, height: 6, background: 'rgba(255,255,255,0.15)'}} />
      <div style={{position: 'absolute', left: X0, top: Y - 3, width: line - X0, height: 6, background: accent}} />
      {steps.map((label, i) => {
        const done = i < active;
        const isActive = i === active;
        const color = isActive ? AMBER : done ? accent : 'rgba(255,255,255,0.4)';
        return (
          <React.Fragment key={i}>
            {isActive ? (
              <div
                style={{
                  position: 'absolute',
                  left: xAt(i) - 22,
                  top: Y - 22,
                  width: 44,
                  height: 44,
                  borderRadius: 10,
                  border: `3px solid ${AMBER}`,
                  opacity: 1 - ring,
                  transform: `scale(${1 + ring * 1.2})`,
                }}
              />
            ) : null}
            <div
              style={{
                position: 'absolute',
                left: xAt(i) - 20,
                top: Y - 20,
                width: 40,
                height: 40,
                borderRadius: 9,
                background: done || isActive ? color : BG,
                border: `4px solid ${color}`,
              }}
            />
            <div
              style={{
                position: 'absolute',
                left: xAt(i) - 130,
                width: 260,
                top: Y + 44,
                textAlign: 'center',
                fontSize: steps.length > 4 ? 26 : 30,
                fontWeight: 700,
                letterSpacing: 3,
                textTransform: 'uppercase',
                color,
              }}
            >
              {label}
            </div>
          </React.Fragment>
        );
      })}

      {/* card */}
      <div
        style={{
          position: 'absolute',
          left: 200,
          top: 830,
          width: 680,
          height: 600,
          borderRadius: 56,
          background: 'rgba(255,255,255,0.05)',
          border: '2px solid rgba(255,255,255,0.14)',
          boxShadow: `0 40px 120px rgba(0,0,0,0.6), inset 0 0 80px ${accent}22`,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 46,
          opacity: card,
          transform: `translateY(${(1 - card) * 80}px)`,
        }}
      >
        <Icon name={props.icon ?? 'lock'} size={230} color={AMBER} stroke={1.4} />
        <div style={{width: 480, height: 18, borderRadius: 9, background: 'rgba(255,255,255,0.12)', overflow: 'hidden'}}>
          <div style={{width: `${bar * 100}%`, height: '100%', background: accent, borderRadius: 9}} />
        </div>
        {props.status ? (
          <div
            style={{
              padding: '14px 34px',
              border: `3px solid ${accent}`,
              borderRadius: 12,
              color: accent,
              fontSize: 38,
              fontWeight: 700,
              letterSpacing: 4,
              textTransform: 'uppercase',
              opacity: status,
              transform: `scale(${0.85 + status * 0.15})`,
            }}
          >
            {props.status}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
