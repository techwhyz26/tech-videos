import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {clamp, pop} from '../theme';
import {Icon} from '../components/Icon';

/** props: { items: string[], hub: { label: string, icon?: string } } - many things that all depend on one. */
export const HubScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items: string[] = (props.items ?? []).slice(0, 7);
  const hub = (props.hub ?? {label: ''}) as {label: string; icon?: string};
  const nTop = Math.ceil(items.length / 2);
  const nBot = items.length - nTop;
  const pos = items.map((_, i) => {
    const topRow = i < nTop;
    const count = topRow ? nTop : nBot;
    const j = topRow ? i : i - nTop;
    return {x: ((j + 0.5) * 1080) / count, y: topRow ? 640 : 790};
  });
  const HX = 540;
  const HY = 1270;
  const R = 150;
  const linesStart = 6 + items.length * 3;
  const reveal = interpolate(frame, [linesStart, linesStart + 22], [0, 1], clamp);
  const h = pop(frame, fps, linesStart + 14);
  const pulse = 1 + Math.sin(frame / 8) * 0.03;

  return (
    <AbsoluteFill>
      <svg width={1080} height={1920} style={{position: 'absolute', inset: 0}}>
        <defs>
          <clipPath id="hub-reveal">
            <rect x={0} y={0} width={1080} height={640 + reveal * (HY - R - 640)} />
          </clipPath>
        </defs>
        <g clipPath="url(#hub-reveal)">
          {pos.map((p, i) => (
            <path
              key={i}
              d={`M ${p.x} ${p.y + 40} C ${p.x} ${p.y + 260}, ${HX + (p.x - HX) * 0.12} ${HY - R - 230}, ${HX + (p.x - HX) * 0.06} ${HY - R + 6}`}
              fill="none"
              stroke="rgba(255,255,255,0.6)"
              strokeWidth={4}
              strokeDasharray="12 14"
              strokeDashoffset={-frame * 1.6}
              strokeLinecap="round"
            />
          ))}
        </g>
      </svg>

      {items.map((label, i) => {
        const t = pop(frame, fps, 3 + i * 3);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: pos[i].x,
              top: pos[i].y - 42,
              height: 84,
              padding: '0 34px',
              display: 'flex',
              alignItems: 'center',
              borderRadius: 42,
              background: '#fff',
              color: '#111',
              fontSize: items.length > 5 ? 32 : 38,
              fontWeight: 600,
              whiteSpace: 'nowrap',
              boxShadow: '0 10px 40px rgba(0,0,0,0.5)',
              opacity: t,
              transform: `translateX(-50%) translateY(${(1 - t) * -50}px)`,
            }}
          >
            {label}
          </div>
        );
      })}

      <div
        style={{
          position: 'absolute',
          left: HX - R,
          top: HY - R,
          width: R * 2,
          height: R * 2,
          borderRadius: '50%',
          background: `radial-gradient(circle at 35% 30%, ${accent}, ${accent}55 70%)`,
          boxShadow: `0 0 140px ${accent}, 0 0 40px ${accent}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: h,
          transform: `scale(${(0.5 + h * 0.5) * pulse})`,
        }}
      >
        <Icon name={hub.icon ?? 'chip'} size={150} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: 80,
          right: 80,
          top: HY + R + 40,
          textAlign: 'center',
          fontSize: 56,
          fontWeight: 700,
          opacity: h,
        }}
      >
        {hub.label}
      </div>
    </AbsoluteFill>
  );
};
