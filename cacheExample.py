import apt
import apt_pkg




deps = []
misspkg = "bison"

# reporting progress
progress = apt.progress.base.OpProgress()
# apt cache
cache = apt_pkg.Cache(progress)
# get the package
pkg = cache[misspkg]
deps.append(misspkg)


depcache = apt_pkg.DepCache(cache)
depcache.init(progress)
pkgmanager = apt_pkg.PackageManager(depcache)


def resolve(pkg, store):
	versions = pkg.version_list
	print(" - Got total {} versions of the package {}".
		format(len(versions), pkg.name))

	for i, v in enumerate(versions[0:1]):
		# print("\nThe {} of all versions: --- {} to be download--- \n"
			# .format(i+1, v.downloadable))
		# get dependencies of thie package version
		depends = v.depends_list.get("Depends")
		if depends:
			for d in depends:
				# get name of the pkg
				pkg = d[-1].target_pkg
				# already satisfied
				auto = depcache.is_auto_installed(pkg)
				
				# print(d[-1].all_targets())
				if not auto:
					if not pkg.name in store:
						print(".. {} is {} installed".format(pkg.name,
						 "auto" if auto else "not auto"))
						store.append(pkg.name)
						new = resolve(pkg,store)
						if new: store=(new)
	return store
print("=== Building dependency tree...")				
deps = resolve(pkg, deps)


#todo
print(deps)


