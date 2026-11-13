# 依 AGENTS.md 的繪圖慣例產生示意圖：長度 1 m = 12 px；線寬 px = 公分 × 0.3（最小 3 px）
M=12; ASP="#3b403e"; GR="#b7c6ae"; W="#f4f4ee"; Y="#e2b40c"; LANE=3.5*M
VW=760
def wpx(cm): return max(3, cm*0.3)
def head(h, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {h}" role="img" aria-label="{title}"><title>{title}</title><rect width="{VW}" height="{h}" fill="{GR}"/>'
def road(y0, n, x0=20, x1=VW-20):
    return f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{n*LANE}" fill="{ASP}"/>'
def solid(y, color=W, cm=10, x0=20, x1=VW-20):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{color}" stroke-width="{wpx(cm)}"/>'
def dash(y, seg, gap, color=W, cm=10, x0=20, x1=VW-20):
    return f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{color}" stroke-width="{wpx(cm)}" stroke-dasharray="{seg*M} {gap*M}"/>'
def double(y, color=W, cm=10, gapcm=10):
    o=(wpx(cm)+gapcm*0.3)/2
    return solid(y-o,color,cm)+solid(y+o,color,cm)
def solid_dash(y, color=W, solid_side="top"):
    o=(wpx(10)+3)/2
    a,b=(y-o,y+o) if solid_side=="top" else (y+o,y-o)
    return solid(a,color)+dash(b,4,6,color)
def label(x,y,t,anchor="start",size=15,color="#1d2321"):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-family="sans-serif">{t}</text>'
def arrow(x,y,right=True):
    d=f"M{x-14},{y} L{x+10},{y} M{x+2},{y-6} L{x+10},{y} L{x+2},{y+6}" if right else f"M{x+14},{y} L{x-10},{y} M{x-2},{y-6} L{x-10},{y} L{x-2},{y+6}"
    return f'<path d="{d}" stroke="#d9dcd8" stroke-width="2.5" fill="none"/>'
def scale(y):
    return f'<line x1="20" y1="{y}" x2="{20+10*M}" y2="{y}" stroke="#1d2321" stroke-width="2"/>'+label(20+10*M+8,y+5,"10 m",size=13)

def svg_165():
    y0=40; s=head(170,"分向限制線示意")+road(y0,2)+solid(y0+2,W,15)+solid(y0+2*LANE-2,W,15)+double(y0+LANE,Y)
    s+=arrow(380,y0+LANE/2,False)+arrow(380,y0+1.5*LANE,True)+label(20,24,"雙黃實線：兩側都不得跨越、不得迴轉")+scale(150)
    return s+"</svg>"
def svg_166():
    y0=40; s=head(170,"單向禁止超車線示意")+road(y0,2)+solid(y0+2,W,15)+solid(y0+2*LANE-2,W,15)+solid_dash(y0+LANE,Y,"top")
    s+=arrow(380,y0+LANE/2,False)+arrow(380,y0+1.5*LANE,True)
    s+=label(20,24,"上方車道靠近實線：禁止超車；下方車道靠近虛線：允許超車")+scale(150)
    return s+"</svg>"
def svg_167():
    y0=40; s=head(220,"禁止變換車道線示意")+road(y0,3)+solid(y0+2,W,15)+solid(y0+3*LANE-2,W,15)
    s+=double(y0+LANE)+solid_dash(y0+2*LANE,W,"top")
    for i in range(3): s+=arrow(380,y0+LANE*(i+.5))
    s+=label(20,24,"上：雙白實線（雙邊）　下：白實線配白虛線（單邊，實線側不得變換）")
    s+=label(VW-30,y0+LANE-8,"雙邊",anchor="end",size=13,color="#fff")+label(VW-30,y0+2*LANE-8,"單邊",anchor="end",size=13,color="#fff")+scale(200)
    return s+"</svg>"
def svg_171():
    y0=40; yE=y0+2*LANE; h=300; s=head(h,"槽化線（斜紋線）示意")+road(y0,2)
    xs,xd,xe=150,380,VW-20; drop=60
    s+=f'<polygon points="20,{yE} {xd},{yE} {xe},{yE} {xe},{yE+drop+LANE} {xd},{yE+LANE} {xs},{yE+LANE}" fill="{ASP}"/>'
    tri=f"{xd},{yE} {xe},{yE} {xe},{yE+drop}"
    s+=f'<clipPath id="g"><polygon points="{tri}"/></clipPath><g clip-path="url(#g)">'
    for x in range(xd-80,xe+20,18):
        s+=f'<line x1="{x}" y1="{yE+drop}" x2="{x+drop}" y2="{yE}" stroke="{W}" stroke-width="6"/>'
    s+="</g>"
    s+=f'<polygon points="{tri}" fill="none" stroke="{W}" stroke-width="{wpx(15)}"/>'
    s+=solid(y0+2,W,15)+dash(y0+LANE,4,6)+dash(yE,1,2,W,30,xs+10,xd)
    s+=f'<polyline points="20,{yE} {xs},{yE+LANE} {xd},{yE+LANE} {xe},{yE+drop+LANE}" fill="none" stroke="{W}" stroke-width="{wpx(15)}"/>'
    s+=arrow(250,y0+LANE/2)+arrow(250,y0+1.5*LANE)+arrow(260,yE+LANE/2)
    s+=label(xe-6,yE+drop+LANE+22,"往匝道",anchor="end",size=14)
    s+=label(20,24,"匝道分流處：斜紋線圍出禁止跨越的區域（斜紋寬 20 cm、間隔 30 cm、45 度；圖中間距放大）")+scale(h-20)
    return s+"</svg>"
def svg_174():
    y0=40; s=head(220,"車種專用車道標線示意")+road(y0,3)+solid(y0+2,W,15)+solid(y0+3*LANE-2,W,15)+dash(y0+LANE,4,6)+double(y0+2*LANE)
    cy=y0+2.5*LANE
    for x in (60,60+40*M):
        s+=f'<polygon points="{x},{cy} {x+1.25*M},{cy-0.5*M} {x+2.5*M},{cy} {x+1.25*M},{cy+0.5*M}" fill="none" stroke="{W}" stroke-width="{wpx(15)}"/>'
    s+=label(60+20*M,cy+5,"大客車專用",anchor="middle",size=13,color="#fff")
    for i in range(3): s+=arrow(380 if i<2 else 600,y0+LANE*(i+.5))
    s+=label(20,24,"外側專用車道：白色菱形（250 × 100 cm），與相鄰車道以雙白實線分隔")+scale(200)
    return s+"</svg>"
def svg_181():
    y0=40; s=head(170,"行車分向線示意")+road(y0,2)+solid(y0+2,W,15)+solid(y0+2*LANE-2,W,15)+dash(y0+LANE,4,6,Y)
    s+=arrow(380,y0+LANE/2,False)+arrow(380,y0+1.5*LANE,True)+label(20,24,"黃虛線：線段 4 m、間距 6 m，劃分雙向車道")+scale(150)
    return s+"</svg>"
def svg_182():
    y0=40; s=head(220,"車道線示意")+road(y0,3)+solid(y0+2,W,15)+solid(y0+3*LANE-2,W,15)+dash(y0+LANE,4,6)+dash(y0+2*LANE,4,6)
    for i in range(3): s+=arrow(380,y0+LANE*(i+.5))
    s+=label(20,24,"白虛線：線段 4 m、間距 6 m，劃分同向車道")+scale(200)
    return s+"</svg>"
def svg_183():
    y0=40; s=head(220,"路面邊線示意")+f'<rect x="20" y="{y0+2*LANE}" width="{VW-40}" height="{2.5*M}" fill="#4a4f4d"/>'+road(y0,2)
    s+=solid(y0+3,W,15)+dash(y0+LANE,4,6)+solid(y0+2*LANE,W,15)
    for i in range(2): s+=arrow(380,y0+LANE*(i+.5))
    s+=label(VW/2,y0+2*LANE+20,"路肩",anchor="middle",size=13,color="#e6e6e0")
    s+=label(20,24,"白實線 15 cm：標示路面外緣或路肩邊緣（比車道線 10 cm 寬）")+scale(200)
    return s+"</svg>"
def svg_183_1():
    y0=40; h=240; s=head(h,"快慢車道分隔線示意")+road(y0,3)+f'<rect x="20" y="{y0+3*LANE}" width="{VW-40}" height="{2*M}" fill="#9aa39c"/>'
    s+=solid(y0+2,Y,10)+dash(y0+LANE,4,6)+solid(y0+2*LANE,W,10)
    for i in range(3): s+=arrow(380,y0+LANE*(i+.5))
    s+=label(VW-30,y0+1.5*LANE+5,"快車道",anchor="end",size=13,color="#fff")+label(VW-30,y0+2.5*LANE+5,"慢車道（≥ 2 m）",anchor="end",size=13,color="#fff")
    s+=label(VW/2,y0+3*LANE+16,"人行道",anchor="middle",size=13)
    s+=label(20,24,"白實線 10 cm：劃分快車道與慢車道，距人行道或路緣至少 2 m")+scale(h-14)
    return s+"</svg>"
def svg_189_1():
    y0=40; s=head(220,"穿越虛線示意")+road(y0,2)+f'<rect x="200" y="{y0+2*LANE}" width="{VW-220}" height="{LANE}" fill="{ASP}"/>'
    s+=solid(y0+2,W,15)+dash(y0+LANE,4,6)+solid(y0+2*LANE,W,15,20,200)+dash(y0+2*LANE,1,2,W,30,200)+solid(y0+3*LANE-2,W,15,200)
    for i in range(2): s+=arrow(300,y0+LANE*(i+.5))
    s+=arrow(600,y0+2.5*LANE)+label(VW-24,y0+2.5*LANE+5,"加速車道",anchor="end",size=13,color="#fff")
    s+=label(20,24,"主線與加速車道之間：白虛線線段 1 m、間距 2 m（較車道線密）")+scale(200)
    return s+"</svg>"
DRAW={"165":svg_165,"166":svg_166,"167":svg_167,"171":svg_171,"174":svg_174,"181":svg_181,"182":svg_182,"183":svg_183,"183-1":svg_183_1,"189-1":svg_189_1}
