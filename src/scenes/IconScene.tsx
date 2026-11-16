import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {display, pop} from '../theme';
import {Icon} from '../components/Icon';

/** props: { icon: string, label?: string, tags?: string[] } - one concept with a glowing icon. */
export const IconScene: React.FC<SceneProps> = ({props, accent}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tags: string[] = (props.tags ?? []).slice(0, 4);
  const t = pop(frame, fps, 2, 10);
  const lab = pop(frame, fps, 12);
  const CY = 930;

  return (
    <AbsoluteFill>
      {[0, 1, 2].map((i) => {
        const p = ((frame + i * 20) % 60) / 60;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 540 - 200,
              top: CY - 200,
              width: 400,
              height: 400,
              borderRadius: '50%',
              border: `3px solid ${accent}`,
              opacity: (1 - p) * 0.5 * t,
              transform: `scale(${1 + p * 0.9})`,
            }}
          />
        );
      })}
      <div
        style={{
          position: 'absolute',
          left: 540 - 200,
          top: CY - 200,
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: `radial-gradient(circle at 35% 30%, ${accent}, ${accent}44 72%)`,
          boxShadow: `0 0 160px ${accent}aa`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: t,
          transform: `scale(${0.4 + t * 0.6})`,
        }}
      >
        <Icon name={props.icon ?? 'bolt'} size={220} />
      </div>
      <div
        style={{
          position: 'absolute',
          left: 60,
          right: 60,
          top: CY + 270,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 40,
        }}
      >
      {props.label ? (
        <div
          style={{
            textAlign: 'center',
            fontFamily: display,
            fontSize: String(props.label).length > 18 ? 84 : 110,
            lineHeight: 1.1,
            textTransform: 'uppercase',
            opacity: lab,
            transform: `translateY(${(1 - lab) * 40}px)`,
          }}
        >
          {props.label}
        </div>
      ) : null}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: 20,
        }}
      >
        {tags.map((tag, i) => {
          const k = pop(frame, fps, 20 + i * 5);
          return (
            <div
              key={i}
              style={{
                padding: '14px 32px',
                borderRadius: 50,
                background: 'rgba(255,255,255,0.1)',
                border: '2px solid rgba(255,255,255,0.2)',
                fontSize: 36,
                fontWeight: 600,
                opacity: k,
                transform: `scale(${0.7 + k * 0.3})`,
              }}
            >
              {tag}
            </div>
          );
        })}
      </div>
      </div>
    </AbsoluteFill>
  );
};
