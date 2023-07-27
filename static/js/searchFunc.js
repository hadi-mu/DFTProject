
document.addEventListener('DOMContentLoaded', function() {
    document.getElementsById('searchIn').onsubmit = function() {



                
        var types=[];
        for(var option of document.getElementById('typeSelection').options){
            if(option.selected){
                types.push(option.value)
            }
        }
        console.log(types)

        var authors=[];
        for(var option of document.getElementById('authorSelection').options){
            if(option.selected){
                authors.push(option.value)
            }
        }
        console.log(authors)


        var sources=[];
        for(var option of document.getElementById('sourceSelection').options){
            if(option.selected){
                sources.push(option.value)
            }
        }
        console.log(sources)



        $.ajax({
            url:'/filter',
            type:'POST',
            data:{
            'types':types,
            'authors':authors,
            'sources':sources
        }
        })


        console.log('Submitted.')
        


        
            };
});



//sends search box content to python file when search submitted

            