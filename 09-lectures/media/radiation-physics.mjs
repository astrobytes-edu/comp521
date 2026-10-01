// Ideal blackbody model; CGS constants match Projects 2 and 3.
export const H=6.62607015e-27, C=2.99792458e10, KB=1.380649e-16;
export const SIGMA=2*Math.PI**5*KB**4/(15*H**3*C**2);
export function wienResidual(x) {return x+5*Math.expm1(-x);}
export function wienDerivative(x) {return 1-5*Math.exp(-x);}
function positivePeakRoot() {
  let lo=4,hi=6;
  for(let n=0;n<60;n++) {const mid=(lo+hi)/2;if(wienResidual(mid)>0)hi=mid;else lo=mid;}
  return (lo+hi)/2;
}
export const WIEN_X=positivePeakRoot(), WIEN_B=H*C/(KB*WIEN_X);
function positive(value,name) {
  if(!Number.isFinite(value)||value<=0)throw new RangeError(name+' must be finite and positive.');
}
export function planckLambda(lambdaCm,temperature) {
  positive(lambdaCm,'Wavelength');positive(temperature,'Temperature');
  const x=H*C/(lambdaCm*KB*temperature);
  // Compute in logs to retain the short-wavelength tail without exponential overflow.
  const logDenominator=x>50?x+Math.log1p(-Math.exp(-x)):Math.log(Math.expm1(x));
  return Math.exp(Math.log(2*H*C*C)-5*Math.log(lambdaCm)-logDenominator);
}
export function planckNu(frequencyHz,temperature) {
  positive(frequencyHz,'Frequency');positive(temperature,'Temperature');
  const x=H*frequencyHz/(KB*temperature);
  const logDenominator=x>50?x+Math.log1p(-Math.exp(-x)):Math.log(Math.expm1(x));
  return Math.exp(Math.log(2*H/(C*C))+3*Math.log(frequencyHz)-logDenominator);
}
export function wavelengthPeak(temperature) {positive(temperature,'Temperature');return WIEN_B/temperature;}
export function surfaceFlux(temperature) {positive(temperature,'Temperature');return SIGMA*temperature**4;}
