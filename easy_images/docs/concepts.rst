====================
Easy Images Concepts
====================


Processor
=========

Process a source image by passing a dictionary of options through a list of 
filters. Each filter looks at the options to decide whether any action is
necessary, returning the altered image if activated.

Image filters
-------------

Accept the image being processed, a dictionary of options (that can be safely
mutated), and a reference to the current batch of images being processed.
Returns the image (after processing if it was required, based on the options
received).

Postprocessors
--------------

Allow the execution of external apps to process the image.

If there are any postprocessors, after all of the filters are run the image is
saved to a temporary local storage location. Each postprocessor called with the
temporary file location and a dictionary of options.

Postprocessors do not need to return the image.


Ledger
======

Keeps track of source, storage, name, and image size.

Encourages the use of aliases (textual representations of a dictionary of
options) that can be set up in the project's settings or via accessing an alias
library.

Can optionally use Django's standard caching system for higher ledger
throughput.

Batch
-----

Rather than processing images independantly, a batch of multiple source images
/ options can be batched together to allow more efficient processing.

Queue
-----

Real-time queues process the image directly, returning it.

Delayed queues use local temporary storage to save queued image (so that the
separate thread processing the image doesn't need to look up the remote
source). They use a JSON string as a messaging protocol which contains the
queued image name and the processed image settings.
