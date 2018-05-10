# Configuration Files

## config.yaml

Holds the main configuration of the project, this will be copied under `~/.librescan` host pc.

## defaultProjectConfig.yaml - probably will deprecate

Holds the basic default configuration of the projects, this will be copied to into every new project
an user creates, if something changes here will affect the next results of the images.

## formsMetadata.yaml

This file defines metadata for forms and inputs that probably an user interface can use.

As this server is just an api service, the user interface can know what to render and what kind
of information send to the server for each form and inputs defined here.

### The format

There is no protocol or standard to do this, we define a convenient way to define the forms metadata.

This describes the inputs of the project, so the interface
can dynamically render the input with its default value

The structure consists in the form name and the children are the inputs.
 Each input can contain attributes like:
        
    type: <string | numeric | range |select | boolean>
    
 - If `type` is `select` you can add extra parameters like:
    - `options`: list of available options
    
    Example:
       
         scantailor:
           orientation:
             type: select
             options:
               - left
               - right
               - upsidedown
               - none
            default: upsidedown
- If `type` is `range` you must specify the `max` and `min` value,
 optionally you can specify the incremental `steps`.
  
  Example:
      
      scantailor:
        depth-perception:
          type: range
          min: 1.0
          max: 3.0
          steps: 0.1
          default: 2.0
 - If type is `string` you can optionally provide a `default` value.
 - If type is `numeric` you can provide a default value.
 - If type is `boolean` you can provide a default value, if not `false` will be the `default`.
  