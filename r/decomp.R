destroy.graph.by.function <- function(graph, fn) {
    g <- graph
    csizes <- c()
    while (vcount(g) > 0) {
        largest.component.size <- max(clusters(g)$csize)
        csizes <- c(csizes, largest.component.size)
        node.id <- fn(g)
        #node.index <- fn(g)
        #max.index <- which.max(fn(g))
        #node.id <- as.vector(V(g))[node.index]
        g <- delete.vertices(g, V(g)[node.id])
    }
    csizes
}

destroy.graph.by.order <- function(graph, v) {
    g <- graph
    csizes <- c()
    for (node.id in v) {
        largest.component.size <- max(clusters(g)$csize)
        csizes <- c(csizes, largest.component.size)
        g <- delete.vertices(g, V(g)[node.id])
    }
    csizes
}

# Delete nodes by degree
#m <- matrix(c(degree(g), as.integer(V(g))), ncol=2)
#nodes.by.degree <- V(g)[m[order(m[,1], decreasing=TRUE),][,2]]$name
#csizes.by.degree <- destroy.graph.by.order(g, nodes.by.degree)
csizes.by.degree <- destroy.graph.by.function(g, function(g) {
    node.index <- which.max(degree(g))
    node.id <- as.vector(V(g))[node.index]
    node.id
})

# Delete nodes by betweeness (dynamic)
csizes.by.betweenness <- destroy.graph.by.function(g, function(g){
    node.index <- which.max(betweenness(g, directed=FALSE))
    node.id <- as.vector(V(g))[node.index]
    node.id
})

# Delete nodes by betweenness (static)
m <- matrix(c(betweenness(g, directed=FALSE), as.integer(V(g))), ncol=2)
nodes.by.betweenness <- V(g)[m[order(m[,1], decreasing=TRUE),][,2]]$name
csizes.by.betweenness.static <- destroy.graph.by.order(g, nodes.by.betweenness)

# Delete nodes by closeness
m <- matrix(c(closeness(g), as.integer(V(g))), ncol=2)
nodes.by.closeness <- V(g)[m[order(m[,1], decreasing=TRUE),][,2]]$name
csizes.by.closeness <- destroy.graph.by.order(g, nodes.by.closeness)

# Delete nodes by commit count
commits <- read.csv("commits.csv", FALSE)
names(commits) <- c("name", "commit.count")
commits$name <- as.character(commits$name)
commits$commit.count <- as.integer(commits$commit.count)
m <- matrix(c(commits$commit.count, V(g)[commits$name]), ncol=2)
nodes.by.commit.count <- V(g)[m[order(m[,1], decreasing=TRUE),][,2]]$name
csizes.by.commit.count <- destroy.graph.by.order(g, nodes.by.commit.count)

# Delete nodes randomly
csizes.by.random <- destroy.graph.by.function(g, function(g) {
    node.id <- sample(as.vector(V(g)), 1)
    node.id
})

# Write the data out to a tab delimited file
results <- matrix(data=c(csizes.by.random, 
						 csizes.by.commit.count, 
						 csizes.by.degree, 
						 csizes.by.closeness,
						 csizes.by.betweenness.static), ncol=5)
write.table(results, "author_network_results.dat", sep="\t")

# Create the chart for by order destruction
png("network_devolutions.png", 800, 800, bg="transparent")
plot(165:1, csizes.by.degree, 
    type="l", col="blue",
    ylim=c(1, 165), xlim=c(165,0),
    main="Network Metrics",
    xlab="Nodes in Graph", ylab="Nodes in Largest Component")
#lines(165:1, csizes.by.betweenness, type="l", col="blue")
lines(165:1, csizes.by.betweenness.static, type="l", col="red")
lines(165:1, csizes.by.closeness, type="l", col="green")
lines(165:1, csizes.by.commit.count, type="l", col="orange")
lines(165:1, csizes.by.random, type="l", col="black")
legend("topright", inset=.05, title="Metric", 
    c("Random", 
      "Commit Count", 
      "Degree", 
      "Betweenness", 
      "Closeness"),
    col=c("black", "orange", "blue", "red", "green"),
    lty=1)
# png("network_devolutions.png", 400, 400, bg="transparent")
# plot(165:1, csizes.by.betweenness.static, 
#     type="l", col="blue",
#     ylim=c(1, 165), xlim=c(165,0),
#     main="Network Metrics",
#     xlab="Nodes in Graph", ylab="Nodes in Largest Component")
# lines(165:1, csizes.by.betweenness, type="l", col="red")
# legend("topright", inset=.05, title="Metric", 
#     c("Betweenness", "Betweenness (dynamic)"),
#     col=c("blue", "red"),
#     lty=1)
grid()
dev.off()
