using Plots
using PyCall
using BenchmarkTools


mutable struct RandomWalker
    row::Int
    col::Int
    moving:: Bool
end


function create_world(n::Int)::Array{Int,2}
    return zeros(Int, n, n)
end


function add_walkers(world::Array{Int, 2}, walkers::Vector{RandomWalker})
    for walker in walkers
        world[walker.row, walker.col] = 1
    end
end


function initialize_walkers(world::Array{Int,2}, n_walkers::Int, n_rows::Int)::Vector{RandomWalker}
    walkers = [RandomWalker(rand(1:n_rows), rand(1:n_rows), true) for i=1:n_walkers]
    add_walkers(world, walkers)
    return walkers
end


function clean_world(world::Array{Int, 2}, walkers::Vector{RandomWalker})
    for walker in walkers
        if !walker.moving
            continue
        end
        world[walker.row, walker.col] = 0
    end
end


function get_neighborhood(walker::RandomWalker, n_rows::Int)
    return [(walker.row, walker.col + 1 <= n_rows ? walker.col + 1 : 1), # top
    (walker.row - 1 > 0 ? walker.row - 1 : n_rows, walker.col), # bottom
    (walker.row, walker.col - 1 > 0 ? walker.col - 1 : n_rows), # left
    (walker.row + 1 <= n_rows ? walker.row + 1 : 1, walker.col)] # right
end


function update_walkers(walkers::Vector{RandomWalker}, world::Array{Int,2}, n_rows::Int)
    walker_n = 1
    for walker in walkers
        if !walker.moving
            continue
        end
        neighbors = get_neighborhood(walker, n_rows)
        p = rand()

        if p<0.25 #right step
            walker.row, walker.col = neighbors[1]
        elseif  p < 0.5 #bottom step
            walker.row, walker.col = neighbors[2]
        elseif p < 0.75 #left step
            walker.row, walker.col = neighbors[3]
        else #top step
            walker.row, walker.col = neighbors[4]
        end
        world[walker.row, walker.col] = 1

        walker_n += 1
    end
end


function check_walkers(world::Array{Int, 2}, walkers::Vector{RandomWalker}, n_rows::Int)
    for walker in walkers
        if !walker.moving
            continue
        end
        neighborhood = get_neighborhood(walker, n_rows)
        cartesian_indices = [CartesianIndex(n) for n in neighborhood]
        if -1 in world[cartesian_indices]
            walker.moving = false
            world[walker.row, walker.col] = -1
        end
    end
end


function walkers_walk(world::Array{Int,2}, walkers::Vector{RandomWalker}, n_rows::Int)
    check_walkers(world, walkers, n_rows)
    clean_world(world, walkers)
    update_walkers(walkers, world, n_rows)
end


function walk(n_rows::Int, n_walkers::Int, n_steps::Int)
    world = create_world(n_rows)
    # seed = initialize_seed(world, n_rows)
    world[div(n_rows, 2) + 1, div(n_rows, 2) + 1] = -1
    walkers = initialize_walkers(world, n_walkers, n_rows)

    @time for i=1:n_steps
        for j in 1:n_rows
            println(world[j,:])
        end
        println("")
        walkers_walk(world, walkers, n_rows)
    end
    world

end

walk(5, 2, 2)

