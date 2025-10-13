import{C as t,a as d}from"./circle-x-DQl-CdHB.js";import{c as r}from"./createLucideIcon-BA_zicjl.js";import{C as g}from"./circle-alert-DgqhRVXg.js";import{c as n,a as m,k as o,g as u,d as p,l as C,m as y,t as k,n as b}from"./index-PcK2SAYs.js";/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const f=r("circle-play",[["path",{d:"M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z",key:"kmsa83"}],["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}]]);/**
 * @license lucide-vue-next v0.545.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const e=r("clock",[["path",{d:"M12 6v6l4 2",key:"mmk7yg"}],["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}]]),S={__name:"StatusBadge",props:{status:{type:String,required:!0},label:{type:String,default:""}},setup(a){const s=a,c={Active:{class:"badge-success",icon:f},Completed:{class:"badge-success",icon:t},Assigned:{class:"badge-info",icon:e},Planned:{class:"badge-info",icon:e},Cancelled:{class:"badge-danger",icon:d},Open:{class:"badge-warning",icon:g},"In Progress":{class:"badge-warning",icon:e},Closed:{class:"badge-success",icon:t}},i=n(()=>c[s.status]?.class||"badge-info"),l=n(()=>c[s.status]?.icon||null);return(v,h)=>(o(),m("span",{class:b(["badge",i.value])},[l.value?(o(),u(y(l.value),{key:0,class:"w-3 h-3 mr-1"})):p("",!0),C(" "+k(a.label),1)],2))}};export{e as C,S as _};
//# sourceMappingURL=StatusBadge-Cp8b1Ujq.js.map
