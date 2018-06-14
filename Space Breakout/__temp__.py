            welkomLabel = gb.fontobjTITEL.render('SPACE BREAKOUT!', True, gb.white,gb.black)

            gb.menuSurface.blit(welkomLabel,(400-int(welkomLabel.get_width()/2),50))
            gb.menuSurface.blit(uitlegLijn1Label,(400-int(uitlegLijn1Label.get_width()/2),150))
            gb.menuSurface.blit(uitleglijn2Label,(400-int(uitleglijn2Label.get_width()/2),180))
            gb.menuSurface.blit(startLabel,(400-int(startLabel.get_width()/2),300))
stringMenuList = ('Gebruik ARROW KEYS of je MUIS','Druk SPATIE of op je muisknop voor de ball te starten!','Press any key to continue...')
