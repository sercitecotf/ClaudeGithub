import{r,a as p}from"./react-Bz8H_8HO.js";import{R as T}from"./react-router-DlC08gwv.js";import{c as w}from"./@remix-run-BYjvVr8v.js";/**
 * React Router DOM v6.16.0
 *
 * Copyright (c) Remix Software Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.md file in the root directory of this source tree.
 *
 * @license MIT
 */const b="startTransition",l=p[b];function y(t){let{basename:f,children:S,future:R,window:h}=t,o=r.useRef();o.current==null&&(o.current=w({window:h,v5Compat:!0}));let e=o.current,[i,s]=r.useState({action:e.action,location:e.location}),{v7_startTransition:n}=R||{},a=r.useCallback(c=>{n&&l?l(()=>s(c)):s(c)},[s,n]);return r.useLayoutEffect(()=>e.listen(a),[e,a]),r.createElement(T,{basename:f,children:S,location:i.location,navigationType:i.action,navigator:e})}var u;(function(t){t.UseScrollRestoration="useScrollRestoration",t.UseSubmit="useSubmit",t.UseSubmitFetcher="useSubmitFetcher",t.UseFetcher="useFetcher"})(u||(u={}));var m;(function(t){t.UseFetchers="useFetchers",t.UseScrollRestoration="useScrollRestoration"})(m||(m={}));export{y as B};
