import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {clamp, pop} from '../theme';

/** props: { source?: string, date?: string, headline: string, body?: string } - a news or document card with a highlighter swipe. */
export const CardScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = pop(frame, fps, 2, 12);
  const swipe = interpolate(frame, [16, 38], [0, 100], clamp);
  const headline: string = props.headline ?? '';

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 110,
          top: 600,
          width: 860,
          padding: '56px 60px 64px',
          borderRadius: 36,
          background: '#f6f4ef',
          color: '#141414',
          boxShadow: `0 60px 160px rgba(0,0,0,0.75), 0 0 0 10px ${accent}55`,
          opacity: t,
          transform: `translateY(${(1 - t) * 200}px) rotate(${-2 + (1 - t) * -6}deg)`,
        }}
      >
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 34}}>
          <span
            style={{
              fontSize: 30,
              fontWeight: 700,
              letterSpacing: 4,
              textTransform: 'uppercase',
              padding: '8px 20px',
              borderRadius: 10,
              background: '#141414',
              color: '#fff',
            }}
          >
            {props.source ?? 'News'}
          </span>
          <span style={{fontSize: 30, fontWeight: 500, color: '#777'}}>{props.date ?? ''}</span>
        </div>
        <div
          style={{
            fontSize: headline.length > 70 ? 54 : 66,
            fontWeight: 700,
            lineHeight: 1.18,
            display: 'inline',
            backgroundImage: `linear-gradient(${accent}88, ${accent}88)`,
            backgroundRepeat: 'no-repeat',
            backgroundSize: `${swipe}% 100%`,
            boxDecorationBreak: 'clone',
            WebkitBoxDecorationBreak: 'clone',
          }}
        >
          {headline}
        </div>
        {props.body ? (
          <div style={{fontSize: 36, fontWeight: 500, lineHeight: 1.4, color: '#555', marginTop: 34}}>
            {props.body}
          </div>
        ) : (
          <div style={{marginTop: 44, display: 'flex', flexDirection: 'column', gap: 20}}>
            {[100, 92, 97, 60].map((w, i) => (
              <div key={i} style={{width: `${w}%`, height: 18, borderRadius: 9, background: '#dcd8cf'}} />
            ))}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
