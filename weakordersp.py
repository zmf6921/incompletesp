# File: weakordersp.py
# Authors: Zack Fitzsimmons (zfitzsim@holycross.edu),
#          Martin Lackner (lackner@dbai.tuwien.ac.at)


import sys
import preflibtools.io as preflibio
import consones


def create_matrix(preference, cands, sp_type):
    num_cands = len(cands)
    pref_mat = []
    for i in range(len(cands)):
        pref_mat.append([0]*len(cands))

    for i, a in enumerate(cands):
        for j, b in enumerate(cands):
            # Lower value denotes a preferred to b
            if preference[a] < preference[b]:
                pref_mat[i][j] = 0
            else:
                pref_mat[i][j] = 1

    # Extensions found in Constructions 2 and 3
    if sp_type == 1 or sp_type == 2:
        # Candidate index for each candidate ranked at each position
        positions = []
        for i in range(len(cands)):
            positions.append([])
        for indx, c in enumerate(cands):
            positions[preference[c]-1].append(indx)

        for curr in range(len(positions)):
            # More than two candidates are tied and these are
            #  not the most-preferred candidates
            # or if testing for Black-SP and there is
            #  more than one most-preferred candidate
            if (curr > 0 and len(positions[curr]) > 2) or \
               (curr == 0 and len(positions[curr]) > 1 and sp_type == 2):
                # Return matrix with no solution
                rowA = [0]*num_cands
                rowA[0] = 1
                rowA[1] = 1
                rowA[2] = 0

                rowB = [0]*num_cands
                rowB[0] = 1
                rowB[1] = 0
                rowB[2] = 1

                rowC = [0]*num_cands
                rowC[0] = 0
                rowC[1] = 1
                rowC[2] = 1

                pref_mat.append(rowA)
                pref_mat.append(rowB)
                pref_mat.append(rowC)
                return pref_mat
            # Exactly two candidates tied and not the most-preferred candidates
            elif (curr > 0 and len(positions[curr]) == 2):
                rowA = [0]*num_cands
                rowB = [0]*num_cands
                rowC = [0]*num_cands

                # Column for first candidate
                rowA[positions[curr][0]] = 0
                rowB[positions[curr][0]] = 1
                rowC[positions[curr][0]] = 1

                # Column for second candidate
                rowA[positions[curr][1]] = 1
                rowB[positions[curr][1]] = 1
                rowC[positions[curr][1]] = 0

                # Candidates preferred to both tied candidates set to 1.
                # Other positions already set to 0.
                #
                # For each position up to curr
                for x in range(curr):
                    # For each candidate ranked at position n
                    # (positions[][] contains candidate indices)
                    for cand_indx in positions[x]:
                        rowA[cand_indx] = 1
                        rowB[cand_indx] = 1
                        rowC[cand_indx] = 1
                pref_mat.append(rowA)
                pref_mat.append(rowB)
                pref_mat.append(rowC)

    return pref_mat


def testsp_file(filename, sp_type, verbose=False):
    print("%s," % (filename), end="")

    election_file = open(filename, 'r')
    try:
        cmap, rmaps, unused_rmapcounts, nvoters = \
            preflibio.read_election_file(election_file)
    except Exception:
        print("0,0,FileError")
        sys.exit(0)
    print("%d,%d," % (len(cmap), nvoters), end="")

    profile_mat = []
    for pref in rmaps:
        pref_mat = create_matrix(pref, cmap, sp_type)
        for row in pref_mat:
            profile_mat.append(row)

    result = consones.solve_sat(profile_mat)
    if result is not None:
        print("True", end="")
    else:
        print("False", end="")

    if verbose:
        print()
        # prints the axis
        if result is not None:
            print("Axis:", [cmap[i+1] for i in result])


if __name__ == "__main__":

    if (len(sys.argv) != 3 or int(sys.argv[2]) not in [0, 1, 2]):
        print("Usage: python3 tryalgo-sp.py election-file N")
        print("N denotes type of SP (Possibly Single-Peaked (0), " +
              "Single-Plateaued (1), or Black Single-Peaked (2).)")
        sys.exit(0)
    filename = str(sys.argv[1])
    sp_type = int(sys.argv[2])
    testsp_file(filename, sp_type, verbose=False)
    print()
