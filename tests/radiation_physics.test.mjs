import test from 'node:test';
import assert from 'node:assert/strict';
import {H,C,KB,SIGMA,WIEN_X,WIEN_B,planckLambda,planckNu,wavelengthPeak,surfaceFlux,wienResidual} from '../09-lectures/media/radiation-physics.mjs';
function close(a,b,tolerance=1e-9){assert.ok(Math.abs(a-b)<=tolerance*Math.abs(b),`${a} vs ${b}`);}
test('Positive root matches the tabulated wavelength displacement constant',()=>{
  close(WIEN_X,4.965114231744276,1e-13);
  close(WIEN_B,.2897771955,1e-9);
  assert.equal(wienResidual(0),0);
  assert.ok(wienResidual(4)<0&&wienResidual(6)>0);
});
test('Peak is a maximum and temperature changes peak and flux by different powers',()=>{
  for(const T of [1000,3000,5000,8000,20000]){
    const peak=wavelengthPeak(T),value=planckLambda(peak,T);
    assert.ok(planckLambda(peak*.99,T)<value&&planckLambda(peak*1.01,T)<value);
    close(wavelengthPeak(2*T),peak/2);close(surfaceFlux(2*T)/surfaceFlux(T),16);
  }
});
test('CGS radiance agrees with an independent direct evaluation and density Jacobian',()=>{
  for(const T of [3000,5000,8000])for(const wavelength of [1e-5,5e-5,1e-4,1e-3]){
    const expected=2*H*C*C/(wavelength**5*Math.expm1(H*C/(wavelength*KB*T)));
    close(planckLambda(wavelength,T),expected);
    close(planckLambda(wavelength,T),C/wavelength**2*planckNu(C/wavelength,T));
    assert.ok(planckLambda(wavelength,T*1.1)>expected);
  }
});
test('Integrating the spectrum independently recovers Stefan–Boltzmann flux',()=>{
  const T=5000,lo=Math.log(1e-7),hi=Math.log(1),n=12000,step=(hi-lo)/n;
  let sum=0;
  for(let j=0;j<=n;j++){
    const lambda=Math.exp(lo+j*step),weight=j===0||j===n?1:j%2?4:2;
    sum+=weight*planckLambda(lambda,T)*lambda;
  }
  close(Math.PI*sum*step/3,SIGMA*T**4,1e-8);
  close(SIGMA,5.670374419e-5,1e-9);
});
test('Invalid physical inputs are rejected and the Wien tail stays finite',()=>{
  for(const value of [0,-1,NaN,Infinity]){
    assert.throws(()=>planckLambda(value,5000),RangeError);
    assert.throws(()=>planckLambda(1e-4,value),RangeError);
    assert.throws(()=>planckNu(value,5000),RangeError);
    assert.throws(()=>wavelengthPeak(value),RangeError);
  }
  assert.equal(planckLambda(1e-8,1000),0);
});
