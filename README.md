Dyet
----

Pseudo-code to Piet source-code transformation.
For lulz and gloriez.

This is a 0.5 version: it generates nice squared images and handle `if`,
`else`, `end` and `while`. I have plans to make it better, but any help will be
appreciated. :)

(See the wiki for monologues and ascii-art about how I plan to implement the
next steps of Dyet.)



Usage
-----

Running `./dyet check/test.dyp > out.ppm` will create an 'out.ppm' file which
is the corresponding Piet code. Run it with npiet and behold!



Pseudo-code specification
-------------------------

In its current basic version, Dyet only support instructions that closely match
the ones explained in Piet documenation. A valid DYP file is therefore just a
list of case-insensitive commands. Comments and whitespace aren't yet supported
at the time of writing.

Are accepted:
  * **push** *arg*,
  * **pop**,
  * **add**,
  * **substract**,
  * **multiply**,
  * **divide**,
  * **mod**,
  * **not**,
  * **greater**,
  * **duplicate**,
  * **roll**,
  * **in_int**,
  * **in_char**,
  * **out_int**,
  * **out_char**

Are also accepted:
  * if [else] end
  * while end



Toolchain
---------

Even if the code doesn't yet reflect the intent, the goal of Dyet is to be
separated in four steps, all centered around the notion of graphs. In Dyet, the
instruction flow is represented as a directed graph: each node represents a
color block (which color should it be, does it need to be of a specific size or
shape...) and each edge represents one of the commands mentioned above.

1. **Parsing**

   During the first step, dyet simply parses the input files and outputs the
   identified tokens. Nothing to fancy here. It'll evolve with the
   pseudo-language specification.

2. **Translation**

   This step takes a list of tokens as input, and outputs the corresponding
   execution graph. For now this graph is trivial, as the accepted input
   commands match the possible edges. But if Dyet starts allowing more complex
   structures, the resulting graph could grow to represent all the possible
   execution path.

   For instance, the *push 42* instruction could be represented by any of those
   graphs:
   * (42) --push-> (*)
   * (2) --push-> (3) --push-> (7) --push-> (*) --mul-> (*) --mul-> (*)
   * (21) --push-> (*) --dup-> (*) --add-> (*)

   An even more advanced translator could even reword the entire tree if it is
   equipped to know the pre and post conditions of some specific
   instructions...

3. **Graph simplification**

   Here will lie the bulk of the code. At this step, the goal will be to reduce
   the generated graph to a linear one. This will involve choosing between many
   execution paths.

4. **Output**

   In this last step, Dyet simply generates an image that represents the chosen
   execution path.
