def split_text(text, chunk_size=1000, overlap=200):

    paragraph=text.split("\n\n")
    chunks=[]
    current_chunk=""

    for para in  paragraph:
        if len(current_chunk)+len(para)>chunk_size:
            chunks.append(current_chunk)
            current_chunk=current_chunk[-overlap:]+"\n\n"+para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    return chunks