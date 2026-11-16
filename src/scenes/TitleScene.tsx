import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');

/** props: { kicker?: string, headline: string, highlight?: string[], sub?: string } */
export const TitleScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const headline: string = props.headline ?? '';
  const words = headline.split(/\s+/).filter(Boolean);
  const hi = new Set<string>((props.highlight ?? []).map(norm));
  const size = headline.length > 34 ? 104 : headline.length > 20 ? 128 : 160;
  const kick = pop(frame, fps, 0);
  const sub = pop(frame, fps, 6 + words.length * 3);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          top: 560,
          left: 80,
          right: 80,
          height: 900,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 44,
        }}
      >
        {props.kicker ? (
          <div
            style={{
              padding: '14px 36px',
              borderRadius: 60,
              border: `3px solid ${accent}`,
              color: accent,
              fontSize: 34,
              fontWeight: 600,
              letterSpacing: 6,
              textTransform: 'uppercase',
              opacity: kick,
              transform: `scale(${0.8 + kick * 0.2})`,
            }}
          >
            {props.kicker}
          </div>
        ) : null}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            columnGap: size * 0.22,
            fontFamily: display,
            fontSize: size,
            lineHeight: 1.08,
            textTransform: 'uppercase',
            textAlign: 'center',
          }}
        >
          {words.map((w, i) => {
            const t = pop(frame, fps, 4 + i * 3);
            return (
              <span
                key={i}
                style={{
                  display: 'inline-block',
                  color: hi.has(norm(w)) ? accent : '#fff',
                  opacity: t,
                  transform: `translateY(${(1 - t) * 60}px)`,
                }}
              >
                {w}
              </span>
            );
          })}
        </div>
        {props.sub ? (
          <div
            style={{
              fontSize: 44,
              fontWeight: 500,
              color: 'rgba(255,255,255,0.7)',
              textAlign: 'center',
              opacity: sub,
              transform: `translateY(${(1 - sub) * 30}px)`,
            }}
          >
            {props.sub}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
