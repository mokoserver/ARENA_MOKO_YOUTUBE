from pathlib import Path
p=Path('/home/user/moko/telegram_avatars/source/build_v02.py');s=p.read_text()
s=s.replace('concept02','concept03').replace('Концепт_02','Концепт_03').replace('КОНЦЕПТ 02','КОНЦЕПТ 03').replace('Концепт 02','Концепт 03').replace('концепт 02','концепт 03').replace('Concept 02','Concept 03').replace("'concept':2","'concept':3")
start=s.index(" s=f'<svg")
end=s.index("\n if kind=='news':",start)
new=''' texture=mark(66,73,225,mono=W,opacity=.10)
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs><pattern id="mokoTexture" width="360" height="310" patternUnits="userSpaceOnUse" patternTransform="rotate(-12 512 512)">{texture}</pattern><radialGradient id="shade" cx=".35" cy=".22" r=".85"><stop offset="0" stop-color="#ffffff" stop-opacity=".03"/><stop offset="1" stop-color="#07111f" stop-opacity=".26"/></radialGradient></defs><rect width="1024" height="1024" fill="{bg}"/>'
 # Broad facets follow the supplied mark; small repeated silhouettes create a brand-specific texture.
 s+=mark(-110,-105,1300,mono='#07111f',opacity=.12)
 s+='<rect width="1024" height="1024" fill="url(#mokoTexture)"/><rect width="1024" height="1024" fill="url(#shade)"/>'
 s+=f'<circle cx="512" cy="512" r="460" fill="none" stroke="{fg}" stroke-width="6" opacity=".14"/>' '''.rstrip()
s=s[:start]+new+s[end:]
start=s.index(' # Deliberately secondary branding')
end=s.index("\n (B/'svg'",start)
new=''' # A shared navy footer carries the original red mark; role icons remain dominant.
 s+='<path d="M0 750L512 785L1024 750V1024H0Z" fill="#0B1220"/><path d="M0 750L512 785L1024 750" fill="none" stroke="#F7F9FC" stroke-width="4" opacity=".17"/>'
 wordw=ns['tw']('MOKO',94,'Jost',500);total=118+25+wordw;x=(1024-total)/2
 s+=mark(x,811,118)+text('MOKO',x+143,888,94,W,'Jost',500)+'</svg>' '''.rstrip()
s=s[:start]+new+s[end:]
s=s.replace('Сначала назначение. Потом бренд.','Разные роли. Фирменная фактура MOKO.')
s=s.replace("font=f(43)","font=f(39)")
s=s.replace('Крупный символ + отдельный цвет всего аватара','Крупный символ · узор из знака MOKO · красный знак на тёмной базе')
s=s.replace("font=f(24),fill='#A4B4C9')","font=f(22),fill='#A4B4C9')")
s=s.replace('Символы теперь главные.\\nMOKO — небольшая подпись.','Цвет и символ — разные.\\nФактура и подпись — общие.')
s=s.replace('Сначала назначение.<br>Потом бренд.','Разные роли.<br>Фирменная фактура MOKO.')
s=s.replace('Вместо шести одинаковых больших знаков MOKO — шесть крупных символов роли. Цвет занимает весь фон. Фирменная подпись остаётся, но больше не мешает различать аватары.','Крупные символы и цвета из второго концепта сохранены. Добавлен узор из исходного знака MOKO, крупные геометрические грани и общая тёмная нижняя часть с красным знаком. Не универсальный шум, а фирменная фактура.')
s=s.replace('MOKO использован как вторичная фирменная подпись, в одноцветной версии.','На нижней тёмной части стоит исходный красный знак MOKO. Фоновый узор повторяет его геометрию в полупрозрачном одноцветном варианте.')
s=s.replace('Концепт 01 сохранён отдельно.','Предыдущие концепты сохранены отдельно.')
s=s.replace('Главное отличие: назначение аватара крупнее бренда. Цвет занимает весь фон. Небольшая подпись MOKO объединяет серию.','Развитие концепта 02: крупные символы и индивидуальные цвета сохранены. Добавлена фирменная фактура из геометрии исходного знака MOKO, крупные грани и общая тёмная нижняя часть с оригинальным красным знаком и светлой надписью MOKO. В малом размере основными ориентирами остаются символ роли, цвет и общая нижняя полоса; мелкий узор не должен быть единственным способом узнавания.')
s=s.replace('Условный макет, не снимок вашего Telegram.','Условный список с вымышленными соседними чатами, не снимок вашего Telegram. Помогает сравнить MOKO с другими аватарами.')
old='''for r in records:s+=f'<div class="row"><img src="{uri(r)}" alt=""><div><strong>{r["title"]}</strong><p>{r["description"]}</p></div></div>' '''.rstrip()
new='''for n,r in enumerate(records):
 s+=f'<div class="row"><img src="{uri(r)}" alt=""><div><strong>{r["title"]}</strong><p>{r["description"]}</p></div></div>'
 if n in [0,2,4]:
  col,initial,lab={0:('#55785c','А','Личный контакт · пример'),2:('#556f89','Д','Другой канал · пример'),4:('#9a6570','Ч','Другой чат · пример')}[n]
  s+=f'<div class="row"><span style="display:grid;place-items:center;width:48px;height:48px;flex-shrink:0;border-radius:50%;background:{col};font-weight:650">{initial}</span><div><strong>{lab}</strong><p>Вымышленный сосед для проверки</p></div></div>' '''.rstrip()
assert old in s;s=s.replace(old,new)
p.with_name('build_v03.py').write_text(s)
