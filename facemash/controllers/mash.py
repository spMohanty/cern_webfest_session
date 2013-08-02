import pprint

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def index():

    """
      mash/index/winner/loser/request ID
      mash/index 
    """
    ###########
    #Defining the Elo Rating Computing Function
    ###########
    ##EloRatingFunction

    def __calculate_elo_rank(player_a_rank=1600, player_b_rank=1600, winner= 1, penalize_loser=True, PLAYER_A = 1, PLAYER_B = 2):
	import math

	if winner is PLAYER_A:
	    winner_rank, loser_rank = player_a_rank, player_b_rank
	else:
	    winner_rank, loser_rank = player_b_rank, player_a_rank
	rank_diff = winner_rank - loser_rank
	exp = (rank_diff * -1) / 400
	odds = 1 / (1 + math.pow(10, exp))
	if winner_rank < 2100:
	    k = 32
	elif winner_rank >= 2100 and winner_rank < 2400:
	    k = 24
	else:
	    k = 16
	new_winner_rank = round(winner_rank + (k * (1 - odds)))
	if penalize_loser:
	    new_rank_diff = new_winner_rank - winner_rank
	    new_loser_rank = loser_rank - new_rank_diff
	else:
	    new_loser_rank = loser_rank
	if new_loser_rank < 1:
	    new_loser_rank = 1
	if winner is PLAYER_A:
	    return (new_winner_rank, new_loser_rank)
	return (new_loser_rank, new_winner_rank)  
    
     
    rows = db(db.face.id!=0).select(limitby=(0,2), orderby='<random>')
    

    if(len(rows)!=2):
        return dict(isValid=False)
    else:
	response.menu.pop()
	response.menu.append((T('Rank List'), False, URL('mash', 'rankList'), []))
        form = FORM(INPUT(_name="face1", value=str(rows[0].id), _type="hidden"),
                    INPUT(_name="face2", value=str(rows[1].id), _type="hidden"),
                    INPUT(_name="selection", _id="mySelection", requires=IS_NOT_EMPTY(), _type="hidden"),
                    INPUT(_type='submit', _id="mySubmit"))

        if form.accepts(request,session):

            face1 = request.vars.face1
            face2 = request.vars.face2

            selection = request.vars.selection

            if selection not in [face1, face2]:
                exit()
            else:
                #update DB
                face1_row = db(db.face.id == int(face1)).select()[0]
                face2_row = db(db.face.id == int(face2)).select()[0]
                
                if face1 == selection:
                    face1_row.won = int(face1_row.won) + 1
                    face2_row.lost = int(face2_row.lost) + 1
                     
                    (face1_row.elo_rating, face2_row.elo_rating) = __calculate_elo_rank(float(face1_row.elo_rating),float(face2_row.elo_rating), winner=face1, penalize_loser=True, PLAYER_A = face1, PLAYER_B = face2)
                else:
                    face2_row.won = int(face2_row.won) + 1
                    face1_row.lost = int(face1_row.lost) + 1
                        
                    (face1_row.elo_rating, face2_row.elo_rating) = __calculate_elo_rank(float(face1_row.elo_rating),float(face2_row.elo_rating), winner=face2, penalize_loser=True, PLAYER_A = face1, PLAYER_B = face2)

                    
                face1_row.update_record()
                face2_row.update_record()
                    
                response.flash = "Whoz your pick !!" ##Replace this by random cheesy lines

        elif form.errors:
                response.flash = "You are trying to do something funny there !! Go try that sumwhere else.."
        else:
                response.flash = "Whoz your pick !!"

        return dict(isValid = True, rows=rows, form=form)

def rankList():
    args = request.args

    if True:
        rows = db(db.face.id > 0).select(orderby=~db.face.elo_rating)
	#response.menu.append((T('Mash'), False, URL('mash', 'index'), []))
	response.menu.pop()

        return dict(isValid = True, rows = rows)
    else:
     	return dict(isValid = False, rows=rows)

def home():
    return dict()
