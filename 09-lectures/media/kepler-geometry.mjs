// Reference geometry for a teaching illustration, not the student Python API.
export const TAU=2*Math.PI;
export const INITIAL_PHASE=(Math.PI/3-.55*Math.sin(Math.PI/3))/TAU;
export function solveKepler(M,e) {
  if(!Number.isFinite(M) || !Number.isFinite(e) || e<0 || e>=1)
    throw new RangeError('Use finite M and 0 <= e < 1.');
  if(e===0 || M===0) return M;
  let lo=M-e,hi=M+e;
  for(let k=0;k<64;k++){
    const mid=lo+(hi-lo)/2,residual=mid-e*Math.sin(mid)-M;
    if(residual===0) return mid;
    if(residual<0)lo=mid;else hi=mid;
  }
  return lo+(hi-lo)/2;
}
export function orbitalState(phase,e) {
  if(!Number.isFinite(phase) || phase<0 || phase>1) throw new RangeError('Phase must be in [0,1].');
  const M=TAU*phase,E=solveKepler(M,e),x=Math.cos(E)-e,y=Math.sqrt(1-e*e)*Math.sin(E);
  let nu=Math.atan2(y,x);if(nu<0)nu+=TAU;if(phase===1)nu=TAU;
  return {M,E,nu,x,y,r:Math.hypot(x,y)};
}
export function orientPosition(x,y,i,omega) {
  const across=x*Math.sin(omega)+y*Math.cos(omega);
  return [x*Math.cos(omega)-y*Math.sin(omega),across*Math.cos(i),across*Math.sin(i)];
}
