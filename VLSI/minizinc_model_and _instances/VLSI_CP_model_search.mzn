include "globals.mzn";

int: width;
int: n;

array[1..n, 1..2] of int: circuits;

array[1..n] of int: areas = [circuits[i, 1] * circuits[i, 2] | i in 1..n];

int: max_height = sum(i in 1..n)(circuits[i, 2]);
int: min_height = max([sum(areas) div width, max(circuits[..,2])]);

var min_height..max_height: height;

array[1..n] of var 0..width: positions_x;
array[1..n] of var 0..max_height: positions_y;

constraint diffn(
  positions_x,
  positions_y,
  circuits[..,1],
  circuits[..,2]
);

constraint forall(i in 1..n)(positions_x[i] + circuits[i, 1] <= width);
constraint forall(i in 1..n)(positions_y[i] + circuits[i, 2] <= height);
constraint height = max([positions_y[i] + circuits[i, 2] | i in 1..n]);

constraint redundant_constraint(
  cumulative(positions_x, circuits[..,1], circuits[..,2], height)
);

constraint redundant_constraint(
  cumulative(positions_y, circuits[..,2], circuits[..,1], width)
);

int: k = min(i in 1..n where areas[i] = max(areas))(i);


constraint symmetry_breaking_constraint(
  positions_x[k] <= (width - circuits[k, 1]) /2
);

constraint symmetry_breaking_constraint(
  positions_y[k]  <= (height - circuits[k, 2]) / 2
);

constraint symmetry_breaking_constraint(
  forall (i in 1..n, j in 1..n where i < j) (
   if circuits[i, 1] == circuits[j, 1] /\ circuits[i, 2] == circuits[j, 2] then
      lex_lesseq([positions_x[i], positions_y[i]],
                 [positions_x[j], positions_y[j]])
    endif
  )
);

% DEFAULT SEARCH
solve minimize height; 


% PREPARING VARIABLES TO SEARCH FOLLOWING THE INPUT ORDER OF CIRCUITS 
/*
  array[1..2*n] of var int: all_vars; 
 constraint forall (i in 1..n)(all_vars[2*i]=positions_y[i] /\ all_vars[2*i-1]=positions_x[i]);
*/

% PREPARING VARIABLES TO SEARCH IN REVERSE ORDER OF CIRCUIT SIZE
/*
array[1..n] of int: perimeters = [circuits[i, 1] + circuits[i, 2] | i in 1..n];
array[1..n] of int: idx =
    sort_by(1..n, [-(perimeters[i]) * (n+1) + i | i in 1..n]);


array[1..2*n] of var int: all_vars; 
constraint forall (i in 1..n)(all_vars[2*i]=positions_y[idx[i]] /\ all_vars[2*i-1]=positions_x[idx[i]]);
*/ 

/*
solve
   ::int_search(
       [height] ++ all_vars,
       input_order,
       indomain_min
     ) minimize height; 

*/
/*
solve
  ::int_search(
      all_vars,
      input_order,
      indomain_min
    ) minimize height;
*/

output [
  "\(width) \(height)\n\(n)\n",
] ++ [
  "\(circuits[i, 1]) \(circuits[i, 2]) \(positions_x[i]) \(positions_y[i])\n"
  | i in 1..n
];
