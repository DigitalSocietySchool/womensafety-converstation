import os
slides = open( 'pimetaslides', 'r' )

for i in slides:
	os.system('convert '+i[:-1]+' -resize 1280x1024 '+i[:-1])
	print 'convert '+i+' -resize 1280x1024 '+i
