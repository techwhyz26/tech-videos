import React from 'react';
import {Composition} from 'remotion';
import {Video} from './Video';
import {Banner, Logo} from './BrandArt';
import type {Spec} from './types';
import {FPS, HEIGHT, WIDTH, totalFrames} from './timeline';
import sample from '../samples/fast-charging.json';

export const Root: React.FC = () => (
  <>
  <Composition id="Logo" component={Logo} width={1080} height={1080} fps={FPS} durationInFrames={1} />
  <Composition id="Banner" component={Banner} width={2560} height={1440} fps={FPS} durationInFrames={1} />
  <Composition
    id="Main"
    component={Video}
    width={WIDTH}
    height={HEIGHT}
    fps={FPS}
    durationInFrames={FPS * 30}
    defaultProps={sample as Spec}
    calculateMetadata={({props}: {props: Spec}) => ({durationInFrames: totalFrames(props)})}
  />
  </>
);
