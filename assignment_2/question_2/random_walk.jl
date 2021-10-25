using Plots
using PyCall
using Distributions
using DelimitedFiles
using BenchmarkTools
using StatsBase
using Dates

plt = pyimport("matplotlib.pyplot")
display = pyimport("IPython.display")

const γ = 5/2
sample_power_law() = round((1 - rand()) ^ (-1/(γ - 1)))

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


function draw_world(world::Array{Int,2})
    plt.cla()
    plt.imshow(world, cmap="cool")
end


function check_spots(spots::Vector{CartesianIndex{2}}, world::Array{Int,2})
    if isempty(spots)
        world .= -1
        exit(0)
    end
end


function initialize_walkers(world::Array{Int,2}, n_walkers::Int, n_rows::Int)::Vector{RandomWalker}
    walkers = Vector{RandomWalker}(undef, n_walkers)
    open_spots = findall(x -> x==0, world)
    check_spots(open_spots, world)

    for i=1:n_walkers
        check_spots(open_spots, world)
        rand_index = rand(1:length(open_spots))
        spot = open_spots[rand_index]
        walkers[i] = RandomWalker(spot[1], spot[2], true)
        deleteat!(open_spots, rand_index)
    end
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


function get_neighborhood(walker::RandomWalker, n_rows::Int, Δ::Int)
    return [(walker.row, (walker.col+Δ) % n_rows == 0 ? n_rows : (walker.col+Δ) % n_rows), # top
    (walker.row - Δ > 0 ? walker.row - Δ : (n_rows + (walker.row - Δ) % n_rows), walker.col), # bottom
    (walker.row, walker.col - Δ > 0 ? walker.col - Δ : (n_rows + (walker.col - Δ) % n_rows)), # left
    ((walker.row+Δ) % n_rows == 0 ? n_rows : (walker.row+Δ) % n_rows, walker.col)] # right
end


function update_walkers(walkers::Vector{RandomWalker}, world::Array{Int,2}, n_rows::Int)
    walker_n = 1
    for walker in walkers
        if !walker.moving
            continue
        end
        Δ = round(Int, sample_power_law())

        neighbors = get_neighborhood(walker, n_rows, Δ)

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

        neighborhood = get_neighborhood(walker, n_rows, 1)
        cartesian_indices = [CartesianIndex(n) for n in neighborhood]
        if -1 in world[cartesian_indices]
            walker.moving = false
            world[walker.row, walker.col] = -1
        end
    end
end


function walkers_walk(world::Array{Int,2}, walkers::Vector{RandomWalker}, n_rows::Int, n_walkers::Int)
    check_walkers(world, walkers, n_rows)
    clean_world(world, walkers)
    update_walkers(walkers, world, n_rows)
end


function walk(n_rows::Int, n_walkers::Int, n_steps::Int)
    folder = pwd()*"/assignment_2/question_2/"*string(now())
    mkdir(folder)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_ylim(0,n_rows)
    ax.set_xlim(0,n_rows)
    ax.set_aspect("equal")

    world = create_world(n_rows)
    world[div(n_rows, 2) + 1, div(n_rows, 2) + 1] = -1
    walkers = initialize_walkers(world, n_walkers, n_rows)

    @time for i=1:n_steps
        walkers_walk(world, walkers, n_rows, n_walkers)
    end
    draw_world(world)
    plt.savefig(folder*"/step_" *string(1)*".png")
    seeds = findall(x -> x==-1, world)
    world[seeds] .= 1
    writedlm(folder*"/grid.csv", world, ',')

end

walk(64, 1000, 1000)
