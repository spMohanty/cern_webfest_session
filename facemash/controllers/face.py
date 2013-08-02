@auth.requires_login()
def create():
    """
    Function to add a new face to a mash
    /face/create/
    """
    def onAccept(form):
        ##Resize uploaded Image here
        def resizeImage(imageName, box):
            #imageName : Name of the imageFile in the uploads directory
            # box : number containing the one edge in pixels of bounding box of the scaled image (always a square)
            import os
            import Image
            
            im = Image.open(request.folder + "uploads/" + imageName)
            w,h = im.size

            if w>h:
                k = box/float(w)
                h = int(k*h)
                w = int(box)
            else :
                k = box/float(h)
                w = int(k*w)
                h = int(box)
            
            im = im.resize((int(w),int(h)),Image.ANTIALIAS)
            im.save(request.folder + "uploads/" + imageName, "JPEG")
            return
            
        resizeImage(form.vars.image, 250)
	#redirect(URL("mash","list",args=mash_id)) #As currently mash/list/[:mash_id] has the only interface to enter images to a mash
    
    form = crud.create(db.face, onaccept=onAccept)
    #form['_action'] = URL("face","create",args=mash_id)
    
    return dict(form = form)
