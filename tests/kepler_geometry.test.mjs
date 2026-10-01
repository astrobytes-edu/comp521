import test from 'node:test';
import assert from 'node:assert/strict';
import {TAU, INITIAL_PHASE, solveKepler, orbitalState, orientPosition} from '../09-lectures/media/kepler-geometry.mjs';

function near(actual, expected, tolerance=2e-13) {
  assert.ok(Math.abs(actual-expected)<tolerance, `${actual} != ${expected}`);
}

test('the shared snapshot distinguishes the center angle from the focus angle',()=>{
  const o=orbitalState(INITIAL_PHASE,.55);
  near(o.E,Math.PI/3);
  near(o.nu,1.639816630833);
  near(o.r,.725);
  near(o.x,-.05);
  assert.ok(o.E<Math.PI/2 && o.nu>Math.PI/2);
});

test('bound ellipses satisfy the independent radius and direction relations',()=>{
  for(const e of [0,.55,.9]) for(let k=0;k<=256;k++){
    const o=orbitalState(k/256,e);
    near(o.E-e*Math.sin(o.E),o.M);
    near(o.r,1-e*Math.cos(o.E));
    near((o.x+e)**2+o.y**2/(1-e*e),1);
    near(Math.cos(o.nu),(Math.cos(o.E)-e)/(1-e*Math.cos(o.E)));
    near(Math.sin(o.nu),Math.sqrt(1-e*e)*Math.sin(o.E)/(1-e*Math.cos(o.E)));
    if(e===0) near(o.nu,o.M);
  }
});

test('unwrapped solves preserve revolutions and both endpoints',()=>{
  for(const turns of [-3,-1,0,2,4]){
    near(solveKepler(TAU*turns+TAU*INITIAL_PHASE,.55),TAU*turns+Math.PI/3);
  }
  near(orbitalState(0,.9).nu,0);
  near(orbitalState(1,.9).nu,TAU);
});

test('the sky rotation preserves radius and the ascending node crosses toward positive Z',()=>{
  for(const i of [0,Math.PI/3,Math.PI/2]) for(const w of [0,Math.PI/2,2.4]){
    const o=orbitalState(INITIAL_PHASE,.55), p=orientPosition(o.x,o.y,i,w);
    near(Math.hypot(...p),o.r);
  }
  assert.ok(orientPosition(1,-1e-5,Math.PI/3,0)[2]<0);
  assert.ok(orientPosition(1, 1e-5,Math.PI/3,0)[2]>0);
  const o=orbitalState(INITIAL_PHASE,.55), p=orientPosition(o.x,o.y,Math.PI/3,Math.PI/2);
  near(p[0],-o.y); near(p[1],o.x/2); near(p[2],o.x*Math.sqrt(3)/2);
});

test('nonfinite and out-of-domain inputs are rejected',()=>{
  for(const e of [NaN,Infinity,-.01,1]) assert.throws(()=>solveKepler(.3,e),RangeError);
  for(const m of [NaN,Infinity,-Infinity]) assert.throws(()=>solveKepler(m,.55),RangeError);
  for(const phase of [NaN,Infinity,-.1,1.1]) assert.throws(()=>orbitalState(phase,.55),RangeError);
});
