import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneProps} from '../types';
import {pop} from '../theme';

/** props: { src: string (file under public/ or an https URL), label?: string, credit?: string } - a photo with a slow zoom. */
export const ImageScene: React.FC<SceneProps> = ({props, accent, frames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const src: string = props.src ?? '';
  const t = pop(frame, fps, 2, 13);
  const zoom = 1.06 + (frame / Math.max(1, frames)) * 0.14;
  const lab = pop(frame, fps, 14);

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: 90,
          top: 560,
          width: 900,
          height: 940,
          borderRadius: 48,
          overflow: 'hidden',
          border: `4px solid ${accent}88`,
          boxShadow: `0 60px 160px rgba(0,0,0,0.7), 0 0 120px ${accent}33`,
          opacity: t,
          transform: `scale(${0.85 + t * 0.15})`,
        }}
      >
        {src ? (
          <Img
            src={/^https?:/.test(src) ? src : staticFile(src)}
            style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}}
          />
        ) : null}
        {props.label ? (
          <div
            style={{
              position: 'absolute',
              left: 36,
              bottom: 36,
              padding: '14px 30px',
              borderRadius: 16,
              background: 'rgba(0,0,0,0.72)',
              fontSize: 40,
              fontWeight: 700,
              opacity: lab,
              transform: `translateX(${(1 - lab) * -40}px)`,
            }}
          >
            {props.label}
          </div>
        ) : null}
      </div>
      {props.credit ? (
        <div
          style={{
            position: 'absolute',
            left: 90,
            right: 90,
            top: 1520,
            fontSize: 24,
            color: 'rgba(255,255,255,0.5)',
          }}
        >
          {props.credit}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
